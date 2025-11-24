"""
Tests para el módulo financiero
"""

from django.test import TestCase
from decimal import Decimal
from .calculos import (
    convertir_tasa_nominal_a_efectiva,
    calcular_cuota_francesa,
    generar_cronograma_pagos,
    calcular_van,
    calcular_tir,
    calcular_relacion_cuota_ingreso
)


class TestConversionTasas(TestCase):
    def test_conversion_nominal_a_efectiva(self):
        tasa_efectiva = convertir_tasa_nominal_a_efectiva(0.12, 12)
        self.assertAlmostEqual(tasa_efectiva, 0.1268, places=4)
    
    def test_conversion_con_cero(self):
        tasa_efectiva = convertir_tasa_nominal_a_efectiva(0, 12)
        self.assertEqual(tasa_efectiva, 0)


class TestCuotaFrancesa(TestCase):
    def test_cuota_basica(self):
        cuota = calcular_cuota_francesa(100000, 0.10, 240)
        self.assertIsInstance(cuota, Decimal)
        self.assertAlmostEqual(float(cuota), 965.02, places=2)
    
    def test_cuota_sin_interes(self):
        cuota = calcular_cuota_francesa(100000, 0, 12)
        esperado = Decimal('8333.33')
        self.assertEqual(cuota, esperado)


class TestCronogramaPagos(TestCase):
    def test_cronograma_sin_gracia(self):
        cronograma = generar_cronograma_pagos(100000, 0.10, 12) 
        self.assertEqual(len(cronograma), 12)
        self.assertEqual(cronograma[0]['tipo'], 'NORMAL')
        self.assertGreater(cronograma[0]['cuota'], 0)
    
    def test_cronograma_con_gracia_total(self):
        cronograma = generar_cronograma_pagos(
            100000, 0.10, 12, tipo_gracia='TOTAL', meses_gracia=3
        )
        
        self.assertEqual(len(cronograma), 15)
        self.assertEqual(cronograma[0]['tipo'], 'GRACIA')
        self.assertEqual(cronograma[0]['cuota'], 0)
        self.assertGreater(cronograma[0]['saldo'], 100000)  # Capitaliza
    
    def test_cronograma_con_gracia_parcial(self):
        cronograma = generar_cronograma_pagos(
            100000, 0.10, 12, tipo_gracia='PARCIAL', meses_gracia=3
        )
        
        self.assertEqual(cronograma[0]['tipo'], 'GRACIA')
        self.assertGreater(cronograma[0]['cuota'], 0)  # Paga solo interés
        self.assertEqual(cronograma[0]['amortizacion'], 0)


class TestIndicadoresFinancieros(TestCase):
    def test_calculo_van(self):
        flujos = [-100000, 30000, 40000, 50000]
        van = calcular_van(flujos, 0.10)
        
        self.assertIsNotNone(van)
        self.assertIsInstance(van, float)
    
    def test_calculo_tir(self):
        flujos = [-100000, 30000, 40000, 50000]
        tir = calcular_tir(flujos)
        
        self.assertIsNotNone(tir)
        self.assertGreater(tir, 0)


class TestRelacionCuotaIngreso(TestCase):
    def test_relacion_normal(self):
        relacion = calcular_relacion_cuota_ingreso(1000, 4000)
        self.assertEqual(relacion, 25.0)
    
    def test_relacion_ingreso_cero(self):
        relacion = calcular_relacion_cuota_ingreso(1000, 0)
        self.assertEqual(relacion, 0.0)