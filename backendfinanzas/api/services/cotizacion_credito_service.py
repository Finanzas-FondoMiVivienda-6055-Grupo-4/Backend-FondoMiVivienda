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
        Este método ahora CALCULA todo antes de GUARDAR.
        """
        # 1. Extraer y convertir datos
        precio_inmueble = float(data['precio_inmueble'])
        cuota_inicial = float(data['monto_inicial'])
        tasa_interes = float(data['tasa_interes'])
        plazo_meses = int(data['plazo_meses'])
        tipo_tasa = data['tipo_tasa']
        
        # 2. Calcular Bono
        monto_bono = 0
        if data.get('aplica_bono_techo_propio') is True:
            monto_bono = CotizacionCreditoService.obtener_bono_buen_pagador(precio_inmueble)
        
        # 3. Calcular Monto a Financiar
        monto_financiar = precio_inmueble - cuota_inicial - monto_bono
        
        # 4. Convertir Tasa (si es nominal, la volvemos efectiva anual)
        tasa_efectiva_anual = tasa_interes
        if tipo_tasa == 'nominal':
            tasa_efectiva_anual = convertir_tasa_nominal_a_efectiva(tasa_interes, 12)

        # 5. Generar Cronograma (Usando el motor del Dev B)
        cronograma_calculado = generar_cronograma_pagos(
            monto_principal=monto_financiar,
            tasa_anual=tasa_efectiva_anual,
            numero_meses=plazo_meses,
            tipo_gracia=data.get('tipo_gracia'),
            meses_gracia=int(data.get('meses_gracia') or 0)
        )

        # 6. Calcular VAN y TIR
        flujos = [-monto_financiar] + [c['cuota'] for c in cronograma_calculado]
        van = calcular_van(flujos, tasa_efectiva_anual)
        tir = calcular_tir(flujos)

        # 7. Completar la data para guardar en BD
        data['monto_financiar'] = monto_financiar
        data['monto_bono_techo_propio'] = monto_bono
        data['tasa_efectiva_anual'] = tasa_efectiva_anual
        data['van_credito'] = van
        data['tir_credito'] = tir
        
        # Totales
        data['total_intereses'] = sum(c['interes'] for c in cronograma_calculado)
        data['total_pagar'] = sum(c['cuota'] for c in cronograma_calculado)
        data['costo_total_credito'] = data['total_pagar'] 
        data['cuota_mensual'] = cronograma_calculado[-1]['cuota'] 
        data['cuota_con_seguros'] = data['cuota_mensual'] # (Ajustar si hay seguros)
        data['tcea'] = tasa_efectiva_anual 
        data['tasa_efectiva_mensual'] = (1 + tasa_efectiva_anual)**(1/12) - 1

        # 8. Guardar Cabecera (Cotizacion)
        nueva_cotizacion = CotizacionCreditoRepository.create(data)

        # 9. Guardar Detalle (Cronograma)
        for cuota_data in cronograma_calculado:
            CronogramaPagoRepository.create({
                'id_cotizacion': nueva_cotizacion,
                'numero_cuota': cuota_data['mes'],
                'fecha_vencimiento': '2025-01-01', 
                'tipo_periodo': cuota_data['tipo'].lower() if cuota_data['tipo'] == 'NORMAL' else 'gracia_' + cuota_data['tipo'].lower(),
                'saldo_inicial': cuota_data['saldo'] + cuota_data['amortizacion'], 
                'interes': cuota_data['interes'],
                'amortizacion': cuota_data['amortizacion'],
                'cuota': cuota_data['cuota'],
                'saldo_final': cuota_data['saldo']
            })
            
        return nueva_cotizacion