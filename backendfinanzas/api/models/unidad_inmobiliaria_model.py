from django.db import models
from api.models import ProyectoInmobiliario

class UnidadInmobiliaria(models.Model):
    id_unidad = models.AutoField(primary_key=True)

    id_proyecto = models.ForeignKey(
        ProyectoInmobiliario,
        on_delete=models.PROTECT,
        related_name="unidades",
        db_column="id_proyecto"
    )

    codigo_unidad = models.CharField(max_length=20, null=True, blank=True)

    TIPO_UNIDAD_CHOICES = [
        ('departamento', 'Departamento'),
        ('casa', 'Casa'),
    ]
    tipo_unidad = models.CharField(max_length=20, choices=TIPO_UNIDAD_CHOICES)

    area_construida = models.DecimalField(max_digits=8, decimal_places=2)
    area_total = models.DecimalField(max_digits=8, decimal_places=2)

    num_dormitorios = models.IntegerField()
    num_banos = models.IntegerField()
    num_estacionamientos = models.IntegerField(null=True, blank=True)

    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)

    MONEDA_CHOICES = [
        ('PEN', 'PEN'),
        ('USD', 'USD'),
    ]
    moneda_precio = models.CharField(max_length=3, choices=MONEDA_CHOICES)

    inicial_minima_porc = models.DecimalField(max_digits=5, decimal_places=2)

    elegible_bono_techo_propio = models.BooleanField(null=True, blank=True)
    monto_bono_disponible = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('separada', 'Separada'),
        ('vendida', 'Vendida'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, null=True, blank=True)

    class Meta:
        db_table = "unidades_inmobiliarias"

    def __str__(self):
        return self.codigo_unidad or f"Unidad {self.id_unidad}"
