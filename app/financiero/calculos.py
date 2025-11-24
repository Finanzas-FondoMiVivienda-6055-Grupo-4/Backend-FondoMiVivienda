from decimal import Decimal, ROUND_HALF_UP
import numpy as np


def convertir_tasa_nominal_a_efectiva(tasa_nominal, periodos_por_anio=12):
    """
    Convierte tasa nominal anual a tasa efectiva anual
    Fórmula: TEA = (1 + TNA/m)^m - 1
    
    Args:
        tasa_nominal (float): Tasa nominal anual (ejemplo: 0.12 para 12%)
        periodos_por_anio (int): Número de períodos en un año (default: 12)
    
    Returns:
        float: Tasa efectiva anual
    
    Ejemplo:
        convertir_tasa_nominal_a_efectiva(0.12, 12)
        0.1268  # 12.68%
    """
    tasa_efectiva = (1 + tasa_nominal / periodos_por_anio) ** periodos_por_anio - 1
    return tasa_efectiva


def convertir_tasa_efectiva_a_nominal(tasa_efectiva, periodos_por_anio=12):
    """
    Convierte tasa efectiva anual a tasa nominal anual
    
    Fórmula: TNA = m * ((1 + TEA)^(1/m) - 1)
    
    Args:
        tasa_efectiva (float): Tasa efectiva anual
        periodos_por_anio (int): Número de períodos en un año
    
    Returns:
        float: Tasa nominal anual
    """
    tasa_nominal = periodos_por_anio * ((1 + tasa_efectiva) ** (1/periodos_por_anio) - 1)
    return tasa_nominal


def calcular_cuota_francesa(monto_principal, tasa_anual, numero_meses):
    """
    Calcula la cuota constante según el sistema francés
    
    Fórmula: R = P * [i(1+i)^n] / [(1+i)^n - 1]
    
    Args:
        monto_principal (float): Monto del préstamo
        tasa_anual (float): Tasa de interés anual (ejemplo: 0.10 para 10%)
        numero_meses (int): Número total de meses del préstamo
    
    Returns:
        Decimal: Cuota mensual constante
    
    Ejemplo:
        calcular_cuota_francesa(100000, 0.10, 240)
        Decimal('965.02')
    """
    if numero_meses == 0:
        return Decimal('0')
    tasa_mensual = tasa_anual / 12
    
    if tasa_mensual == 0:
        return Decimal(str(monto_principal / numero_meses)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
    
    numerador = tasa_mensual * (1 + tasa_mensual) ** numero_meses
    denominador = (1 + tasa_mensual) ** numero_meses - 1
    cuota = monto_principal * (numerador / denominador)
    return Decimal(str(cuota)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def generar_cronograma_pagos(
    monto_principal,
    tasa_anual,
    numero_meses,
    tipo_gracia=None,
    meses_gracia=0
):
    """
    Genera el cronograma completo de pagos
    
    Args:
        monto_principal (float): Monto del préstamo
        tasa_anual (float): Tasa de interés anual
        numero_meses (int): Número de meses del préstamo
        tipo_gracia (str): 'TOTAL', 'PARCIAL' o None
        meses_gracia (int): Número de meses de gracia
    
    Returns:
        list: Lista de diccionarios con el cronograma
    
    Estructura de retorno:
        [
            {
                'mes': 1,
                'saldo': 100000.00,
                'interes': 833.33,
                'amortizacion': 0.00,
                'cuota': 0.00,
                'tipo': 'GRACIA'
            },
            ...
        ]
    """
    tasa_mensual = tasa_anual / 12
    cronograma = []
    saldo = float(monto_principal)
    
    for mes in range(1, meses_gracia + 1):
        interes = saldo * tasa_mensual
        
        if tipo_gracia == 'TOTAL':
            saldo += interes
            cuota = 0.0
            amortizacion = 0.0
        elif tipo_gracia == 'PARCIAL':
            cuota = interes
            amortizacion = 0.0
        else:
            cuota = 0.0
            amortizacion = 0.0
        
        cronograma.append({
            'mes': mes,
            'saldo': round(saldo, 2),
            'interes': round(interes, 2),
            'amortizacion': round(amortizacion, 2),
            'cuota': round(cuota, 2),
            'tipo': 'GRACIA'
        })
    
    cuota_normal = float(calcular_cuota_francesa(saldo, tasa_anual, numero_meses))
    for mes in range(meses_gracia + 1, meses_gracia + numero_meses + 1):
        interes = saldo * tasa_mensual
        amortizacion = cuota_normal - interes
        saldo -= amortizacion
        if saldo < 0.01:
            amortizacion += saldo
            saldo = 0.0
        
        cronograma.append({
            'mes': mes,
            'saldo': round(max(saldo, 0), 2),
            'interes': round(interes, 2),
            'amortizacion': round(amortizacion, 2),
            'cuota': round(cuota_normal, 2),
            'tipo': 'NORMAL'
        })
    
    return cronograma


def calcular_van(flujos_caja, tasa_descuento):
    """
    Calcula el Valor Actual Neto (VAN)
    Args:
    flujos_caja (list): Lista de flujos de caja [inicial, flujo1, flujo2, ...]
    tasa_descuento (float): Tasa de descuento (ejemplo: 0.10 para 10%)
    
    Returns:
    float: Valor Actual Neto
    
    Ejemplo:
    flujos = [-100000, 5000, 5000, 5000]  # Inversión inicial negativa
    calcular_van(flujos, 0.10)
    -87566.08
    """
    try:
        import numpy_financial as npf
        van = npf.npv(tasa_descuento, flujos_caja)
    except ImportError:
        van = flujos_caja[0]
        for t, flujo in enumerate(flujos_caja[1:], start=1):
            van += flujo / ((1 + tasa_descuento) ** t)
    return round(van, 2)


def calcular_tir(flujos_caja):
    """
    Calcula la Tasa Interna de Retorno (TIR)
    
    Args:
        flujos_caja (list): Lista de flujos de caja [inicial, flujo1, flujo2, ...]
    
    Returns:
        float: Tasa Interna de Retorno (ejemplo: 0.15 para 15%), o None si no existe.
    """
    try:
        import numpy_financial as npf
        tir = npf.irr(flujos_caja)
    except ImportError:
        tir = calcular_tir_newton(flujos_caja)
    if tir is None or (isinstance(tir, float) and np.isnan(tir)):
        return None
    return round(tir, 6)


def calcular_tir_newton(flujos_caja, iteraciones_max=100, tolerancia=1e-6):
    """
    Calcula TIR usando método Newton-Raphson (fallback)
    
    Args:
        flujos_caja (list): Flujos de caja
        iteraciones_max (int): Máximo de iteraciones
        tolerancia (float): Tolerancia para convergencia
    
    Returns:
        float: TIR aproximada
    """
    tir = 0.1
    for _ in range(iteraciones_max):
        van = sum(fc / (1 + tir) ** t for t, fc in enumerate(flujos_caja))
        derivada = sum(-t * fc / (1 + tir) ** (t + 1) for t, fc in enumerate(flujos_caja))
        
        if abs(derivada) < 1e-10:
            break
        
        nueva_tir = tir - van / derivada
        if abs(nueva_tir - tir) < tolerancia:
            return nueva_tir
        tir = nueva_tir
    return tir


def validar_parametros_prestamo(monto_principal, tasa_anual, numero_meses):
    """
    Valida que los parámetros del préstamo sean válidos
    
    Raises:
        ValueError: Si algún parámetro es inválido
    """
    if monto_principal <= 0:
        raise ValueError("El monto principal debe ser mayor a 0")
    if tasa_anual < 0:
        raise ValueError("La tasa de interés no puede ser negativa")
    if numero_meses <= 0:
        raise ValueError("El número de meses debe ser mayor a 0")
    if numero_meses > 360:
        raise ValueError("El número de meses no puede exceder 360 (30 años)")


def calcular_cuota_inicial_recomendada(valor_propiedad, porcentaje=0.20):
    """
    Calcula la cuota inicial recomendada (típicamente 20% del valor)
    
    Args:
        valor_propiedad (float): Valor de la propiedad
        porcentaje (float): Porcentaje de cuota inicial (default: 0.20)
    
    Returns:
        float: Monto de cuota inicial recomendada
    """
    return round(valor_propiedad * porcentaje, 2)


def calcular_relacion_cuota_ingreso(cuota_mensual, ingreso_mensual):
    """
    Calcula la relación cuota/ingreso
    Típicamente no debe exceder 30-35%
    
    Args:
        cuota_mensual (float): Cuota mensual del préstamo
        ingreso_mensual (float): Ingreso mensual del cliente
    
    Returns:
        float: Porcentaje de la cuota respecto al ingreso
    """
    if ingreso_mensual <= 0:
        return 0.0
    return round((cuota_mensual / ingreso_mensual) * 100, 2)