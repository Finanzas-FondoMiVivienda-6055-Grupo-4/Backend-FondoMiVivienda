from django.db import models
from api.models import CotizacionCredito

class CronogramaPago(models.Model):
    id_cronograma = models.AutoField(primary_key=True)

    id_cotizacion = models.ForeignKey(
        CotizacionCredito,
        on_delete=models.PROTECT,
        related_name="cronograma",
        db_column="id_cotizacion"
    )

    numero_cuota = models.IntegerField()
    fecha_vencimiento = models.DateField()

    TIPO_PERIODO_CHOICES = [
        ('gracia_total', 'Gracia Total'),
        ('gracia_parcial', 'Gracia Parcial'),
        ('normal', 'Normal'),
    ]
    tipo_periodo = models.CharField(max_length=20, choices=TIPO_PERIODO_CHOICES)

    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2)
    amortizacion = models.DecimalField(max_digits=10, decimal_places=2)
    cuota = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_final = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "cronograma_pagos"

    def __str__(self):
        return f"Cronograma {self.id_cronograma} - Cuota {self.numero_cuota}"
