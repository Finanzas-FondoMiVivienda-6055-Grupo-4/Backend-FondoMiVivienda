from django.db import models

class EntidadFinanciera(models.Model):
    id_entidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)

    tasa_min = models.DecimalField(max_digits=6, decimal_places=4)
    tasa_max = models.DecimalField(max_digits=6, decimal_places=4)

    plazo_min_meses = models.IntegerField()
    plazo_max_meses = models.IntegerField()

    permite_gracia = models.BooleanField(null=True, blank=True)

    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, null=True, blank=True)

    class Meta:
        db_table = "entidades_financieras"

    def __str__(self):
        return self.nombre
