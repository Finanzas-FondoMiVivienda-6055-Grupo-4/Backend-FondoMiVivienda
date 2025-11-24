from decimal import Decimal, ROUND_HALF_UP


def redondear_decimal(valor, decimales=2):
    """
    Redondea un valor a un número específico de decimales
    
    Args:
        valor (float): Valor a redondear
        decimales (int): Número de decimales
    
    Returns:
        Decimal: Valor redondeado
    """
    plantilla = '0.' + '0' * decimales
    return Decimal(str(valor)).quantize(Decimal(plantilla), rounding=ROUND_HALF_UP)


def convertir_porcentaje_a_decimal(porcentaje):
    """
    Convierte un porcentaje a decimal
    
    Args:
        porcentaje (float): Porcentaje (ejemplo: 12.5 para 12.5%)
    
    Returns:
        float: Valor decimal (ejemplo: 0.125)
    """
    return porcentaje / 100


def convertir_decimal_a_porcentaje(decimal):
    """
    Convierte un decimal a porcentaje
    
    Args:
        decimal (float): Valor decimal (ejemplo: 0.125)
    
    Returns:
        float: Porcentaje (ejemplo: 12.5 para 12.5%)
    """
    return decimal * 100


def formatear_moneda(monto, simbolo='S/', decimales=2):
    """
    Formatea un monto como moneda
    
    Args:
        monto (float): Monto a formatear
        simbolo (str): Símbolo de moneda
        decimales (int): Número de decimales
    
    Returns:
        str: Monto formateado
    
    Ejemplo:
        >>> formatear_moneda(1234.56)
        'S/ 1,234.56'
    """
    formato = f"{{:,.{decimales}f}}"
    return f"{simbolo} {formato.format(monto)}"


def calcular_dias_entre_fechas(fecha_inicio, fecha_fin):
    """
    Calcula días entre dos fechas
    
    Args:
        fecha_inicio (date): Fecha inicial
        fecha_fin (date): Fecha final
    
    Returns:
        int: Número de días
    """
    delta = fecha_fin - fecha_inicio
    return delta.days


def convertir_tasa_anual_a_diaria(tasa_anual):
    """
    Convierte tasa anual a tasa diaria
    Asume 360 días al año (convención bancaria)
    
    Args:
        tasa_anual (float): Tasa anual
    
    Returns:
        float: Tasa diaria
    """
    return tasa_anual / 360