from django.db import transaction
from api.repositories.cotizacion_credito_repository import CotizacionCreditoRepository
from api.repositories.cronograma_pago_repository import CronogramaPagoRepository
# Importamos las fórmulas matemáticas de la carpeta financiero
from financiero.calculos import (
    generar_cronograma_pagos, 
    calcular_van, 
    calcular_tir,
    convertir_tasa_nominal_a_efectiva
)

class CotizacionCreditoService:

    @staticmethod
    def listar():
        return CotizacionCreditoRepository.list_all()

    @staticmethod
    def obtener(id_cotizacion: int):
        return CotizacionCreditoRepository.get_by_id(id_cotizacion)

    @staticmethod
    def eliminar(instance):
        CotizacionCreditoRepository.delete(instance)

    # --- LÓGICA DE NEGOCIO  ---

    @staticmethod
    def obtener_bono_buen_pagador(precio_vivienda):
        """
        Retorna el bono referencial (según rangos Mivivienda/Techo Propio)
        """
        if 67300 <= precio_vivienda <= 96300:
            return 25700
        elif 96300 < precio_vivienda <= 139400:
            return 21400
        elif 139400 < precio_vivienda <= 232200:
            return 19600
        elif 232200 < precio_vivienda <= 343900:
            return 7300
        else:
            return 0

    @staticmethod
    @transaction.atomic
    def registrar(data: dict):
        """
        Calcula todo (monto financiar, bono, cronograma, VAN, TIR, TCEA, etc.)
        antes de guardar la cotización y su cronograma.
        """

        # ============= 1) EXTRACCIÓN Y CONVERSIÓN DE DATOS BÁSICOS =============
        precio_inmueble = float(data['precio_inmueble'])
        cuota_inicial   = float(data['monto_inicial'])
        tasa_interes    = float(data['tasa_interes'])   # YA VIENE EN DECIMAL (0.10 = 10%)
        plazo_meses     = int(data['plazo_meses'])
        tipo_tasa       = data.get('tipo_tasa', 'nominal')
        capitalizacion  = data.get('capitalizacion', 'mensual')  # 'mensual' | 'anual'

        # meses por año según capitalización
        if capitalizacion == 'anual':
            periodos_por_anio = 1
        else:
            periodos_por_anio = 12  # mensual por defecto

        # ============= 2) BONO TECHO PROPIO =============
        monto_bono = 0.0
        if data.get('aplica_bono_techo_propio') is True:
            monto_bono = CotizacionCreditoService.obtener_bono_buen_pagador(precio_inmueble)

        # ============= 3) MONTO A FINANCIAR =============
        monto_financiar = precio_inmueble - cuota_inicial - monto_bono

        # ============= 4) TASA EFECTIVA ANUAL =============
        # si es nominal, la convertimos a efectiva anual
        tasa_efectiva_anual = tasa_interes
        if tipo_tasa == 'nominal':
            tasa_efectiva_anual = convertir_tasa_nominal_a_efectiva(
                tasa_interes,
                periodos_por_anio=periodos_por_anio
            )

        # ============= 5) TIPO DE GRACIA Y MESES DE GRACIA =============
        # del front viene 'total' / 'parcial' / 'ninguno'
        tipo_gracia_raw = (data.get('tipo_gracia') or '').upper()
        if tipo_gracia_raw not in ['TOTAL', 'PARCIAL']:
            tipo_gracia = None
        else:
            tipo_gracia = tipo_gracia_raw

        meses_gracia = int(data.get('meses_gracia') or 0)

        # ============= 6) GENERAR CRONOGRAMA SIN SEGUROS (CAPITAL + INTERÉS) =============
        cronograma_calculado = generar_cronograma_pagos(
            monto_principal=monto_financiar,
            tasa_anual=tasa_efectiva_anual,
            numero_meses=plazo_meses,
            tipo_gracia=tipo_gracia,
            meses_gracia=meses_gracia
        )

        # ============= 7) SEGUROS Y GASTOS =============
        # seguros vienen como porcentaje (ej: "2" -> 2% anual)
        def _parse_pct(value):
            if value is None or value == '':
                return 0.0
            v = float(value)
            if v > 1:   # 10 -> 0.10
                v = v / 100.0
            return v

        seguro_incendio_anual    = _parse_pct(data.get('seguro_incendio'))
        seguro_desgravamen_anual = _parse_pct(data.get('seguro_desgravamen'))

        gastos_notariales  = float(data.get('gastos_notariales')  or 0)
        gastos_registrales = float(data.get('gastos_registrales') or 0)
        comision_apertura  = float(data.get('comision_apertura')  or 0)

        # ============= 8) CONSTRUCCIÓN DE FLUJOS CON SEGUROS (PERSPECTIVA CLIENTE) =============
        cuotas_sin_seguro   = []
        cuotas_con_seguros  = []
        total_intereses     = 0.0

        for cuota in cronograma_calculado:
            # saldo "inicial" aproximado del periodo
            saldo_inicial_aprox = cuota['saldo'] + cuota['amortizacion']

            interes   = cuota['interes']
            total_intereses += interes

            # seguros mensuales aproximados
            prima_desgravamen = saldo_inicial_aprox * (seguro_desgravamen_anual / 12.0)
            prima_incendio    = precio_inmueble        * (seguro_incendio_anual    / 12.0)

            cuota_base = cuota['cuota']
            cuota_total = cuota_base + prima_desgravamen + prima_incendio

            cuotas_sin_seguro.append(cuota_base)
            cuotas_con_seguros.append(cuota_total)

        # inversión inicial del cliente (perspectiva CLIENTE)
        inversion_inicial = (
            cuota_inicial
            + gastos_notariales
            + gastos_registrales
            + comision_apertura
            - monto_bono
        )

        flujos_cliente = [-inversion_inicial] + cuotas_con_seguros

        # ============= 9) VAN, TIR, TCEA (PERSPECTIVA CLIENTE) =============
        van_cliente = calcular_van(flujos_cliente, tasa_efectiva_anual)
        tir_mensual = calcular_tir(flujos_cliente)

        if tir_mensual is not None:
            # TIR mensual -> TCEA anual
            tcea = (1 + tir_mensual)**12 - 1
        else:
            tcea = tasa_efectiva_anual  # fallback simple

        # ============= 10) CAMPOS CALCULADOS A GUARDAR EN BD =============
        data['monto_financiar']         = monto_financiar
        data['monto_bono_techo_propio'] = monto_bono

        data['tasa_efectiva_anual']   = tasa_efectiva_anual
        data['tasa_efectiva_mensual'] = (1 + tasa_efectiva_anual)**(1/12) - 1

        data['total_intereses']      = total_intereses
        data['total_pagar']          = sum(cuotas_con_seguros)
        data['costo_total_credito']  = data['total_pagar']  # aquí ya incluye seguros

        # cuota "típica": tomamos la última cuota normal con seguros
        data['cuota_mensual']      = cronograma_calculado[-1]['cuota']
        data['cuota_con_seguros']  = cuotas_con_seguros[-1]

        data['van_credito'] = van_cliente
        data['tir_credito'] = tir_mensual if tir_mensual is not None else 0.0
        data['tcea']        = tcea

        # (Opcional futuro) ratio_cuota_ingreso: requiere ingreso_mensual del cliente
        # -> se puede calcular aquí si se pasa ese dato en "data"

        # ============= 11) GUARDAR CABECERA (COTIZACIÓN) =============
        nueva_cotizacion = CotizacionCreditoRepository.create(data)

        # ============= 12) GUARDAR DETALLE (CRONOGRAMA) =============
        for cuota_data in cronograma_calculado:
            CronogramaPagoRepository.create({
                'id_cotizacion':   nueva_cotizacion,
                'numero_cuota':    cuota_data['mes'],
                'fecha_vencimiento': '2025-01-01',  # TODO: calcular según fecha base
                'tipo_periodo':    cuota_data['tipo'].lower() if cuota_data['tipo'] == 'NORMAL'
                                    else 'gracia_' + cuota_data['tipo'].lower(),
                'saldo_inicial':   cuota_data['saldo'] + cuota_data['amortizacion'],
                'interes':         cuota_data['interes'],
                'amortizacion':    cuota_data['amortizacion'],
                'cuota':           cuota_data['cuota'],   # sin seguros
                'saldo_final':     cuota_data['saldo'],
            })

        return nueva_cotizacion
