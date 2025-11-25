from django.db import models

class Configuracion(models.Model):
    id_config = models.AutoField(primary_key=True)

    MONEDA_CHOICES = [
        ('PEN', 'PEN'),
        ('USD', 'USD'),
    ]
    moneda_defecto = models.CharField(max_length=3, choices=MONEDA_CHOICES, null=True, blank=True)

    tipo_cambio_usd = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)

    TIPO_TASA_CHOICES = [
        ('nominal', 'Nominal'),
        ('efectiva', 'Efectiva'),
    ]
    tipo_tasa_defecto = models.CharField(max_length=10, choices=TIPO_TASA_CHOICES, null=True, blank=True)

    CAPITALIZACION_CHOICES = [
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ]
    capitalizacion_defecto = models.CharField(max_length=10, choices=CAPITALIZACION_CHOICES, null=True, blank=True)

    permite_gracia_total = models.BooleanField(null=True, blank=True)
    permite_gracia_parcial = models.BooleanField(null=True, blank=True)
    max_meses_gracia = models.IntegerField(null=True, blank=True)

    tasa_descuento_van = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    dias_anio = models.IntegerField(null=True, blank=True)

    ratio_cuota_ingreso_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    seguro_incendio_tasa = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)

    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "configuracion"

    def __str__(self):
        return f"Config {self.id_config}"
