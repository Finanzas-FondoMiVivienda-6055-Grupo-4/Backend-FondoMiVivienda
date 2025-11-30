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
        # 12% nominal anual con capitalización mensual ≈ 12.68% efectiva
        self.assertAlmostEqual(tasa_efectiva, 0.1268, places=4)

    def test_conversion_con_cero(self):
        tasa_efectiva = convertir_tasa_nominal_a_efectiva(0, 12)
        self.assertEqual(tasa_efectiva, 0)


class TestCuotaFrancesa(TestCase):
    def test_cuota_basica(self):
        """
        Para un préstamo de 100000 a 10% anual en 240 meses,
        la cuota francesa debería ser ≈ 965.02
        """
        cuota = calcular_cuota_francesa(100000, 0.10, 240)
        self.assertIsInstance(cuota, Decimal)
        self.assertAlmostEqual(float(cuota), 965.02, places=2)

    def test_cuota_sin_interes(self):
        """
        Sin interés, la cuota debería ser simplemente monto / meses.
        """
        cuota = calcular_cuota_francesa(100000, 0, 12)
        esperado = Decimal('8333.33')
        self.assertEqual(cuota, esperado)


class TestCronogramaPagos(TestCase):
    def test_cronograma_sin_gracia(self):
        """
        Cronograma simple sin periodo de gracia.
        Debe tener tantos periodos como meses y la primera fila debe ser NORMAL.
        """
        cronograma = generar_cronograma_pagos(100000, 0.10, 12)
        self.assertEqual(len(cronograma), 12)
        self.assertEqual(cronograma[0]['tipo'], 'NORMAL')
        self.assertGreater(cronograma[0]['cuota'], 0)

    def test_cronograma_con_gracia_total(self):
        """
        En gracia TOTAL se capitalizan intereses:
        - Los primeros 'meses_gracia' periodos son de tipo GRACIA.
        - La cuota es 0 en esos periodos.
        - El saldo aumenta respecto al monto original.
        """
        cronograma = generar_cronograma_pagos(
            100000, 0.10, 12, tipo_gracia='TOTAL', meses_gracia=3
        )

        self.assertEqual(len(cronograma), 15)
        self.assertEqual(cronograma[0]['tipo'], 'GRACIA')
        self.assertEqual(cronograma[0]['cuota'], 0)
        self.assertGreater(cronograma[0]['saldo'], 100000)  # Capitaliza

    def test_cronograma_con_gracia_parcial(self):
        """
        En gracia PARCIAL se paga solo interés:
        - tipo GRACIA
        - cuota > 0
        - amortización = 0
        """
        cronograma = generar_cronograma_pagos(
            100000, 0.10, 12, tipo_gracia='PARCIAL', meses_gracia=3
        )

        self.assertEqual(cronograma[0]['tipo'], 'GRACIA')
        self.assertGreater(cronograma[0]['cuota'], 0)  # Paga solo interés
        self.assertEqual(cronograma[0]['amortizacion'], 0)

    def test_cronograma_consistente_con_cuota_francesa(self):
        """
        Test adicional de diagnóstico:
        Verifica que el cronograma sin gracia sea consistente con la cuota francesa:
        - La cuota del cronograma coincide con la cuota calculada.
        - El saldo del primer periodo corresponde a: saldo = saldo_anterior*(1+i) - cuota
        - El saldo final es cercano a 0.
        """
        monto = 100000
        tasa_anual = 0.10
        meses = 12

        cronograma = generar_cronograma_pagos(monto, tasa_anual, meses)

        # Cuota teórica según la fórmula francesa
        cuota_teorica = calcular_cuota_francesa(monto, tasa_anual, meses)
        cuota_cronograma = cronograma[0]['cuota']

        self.assertAlmostEqual(
            float(cuota_cronograma),
            float(cuota_teorica),
            places=2,
            msg=(
                "[CRONOGRAMA] La cuota del primer periodo no coincide con la cuota francesa. "
                f"Teórica={float(cuota_teorica):.2f}, Cronograma={float(cuota_cronograma):.2f}"
            ),
        )

        # Verificar saldo del primer periodo
        tasa_mensual = tasa_anual / 12
        saldo_esperado_primer_periodo = round(
            monto * (1 + tasa_mensual) - float(cuota_teorica),
            2,
        )
        saldo_primer_periodo = round(float(cronograma[0]['saldo']), 2)

        self.assertAlmostEqual(
            saldo_primer_periodo,
            saldo_esperado_primer_periodo,
            places=2,
            msg=(
                "[CRONOGRAMA] El saldo del primer periodo no coincide con el esperado "
                "(después de la primera cuota). "
                f"Esperado={saldo_esperado_primer_periodo}, Obtenido={saldo_primer_periodo}"
            ),
        )

        # Verificar que el saldo final sea cercano a 0
        saldo_final = float(cronograma[-1]['saldo'])
        self.assertAlmostEqual(
            saldo_final,
            0.0,
            delta=1.0,
            msg=(
                "[CRONOGRAMA] El saldo final debería ser cercano a 0. "
                f"Obtenido={saldo_final}"
            ),
        )


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
