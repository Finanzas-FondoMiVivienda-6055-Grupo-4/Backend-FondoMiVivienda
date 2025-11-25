from django.db import models
from api.models import Cliente, EntidadFinanciera, Usuario

class CotizacionCredito(models.Model):
    id_cotizacion = models.AutoField(primary_key=True)
    codigo_cotizacion = models.CharField(max_length=30, null=True, blank=True)

    # FKs según diagrama
    id_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="cotizaciones",
        db_column="id_cliente"
    )

    # No hay tabla unidades en el diagrama -> por ahora int simple
    id_unidad = models.IntegerField()

    id_entidad = models.ForeignKey(
        EntidadFinanciera,
        on_delete=models.PROTECT,
        related_name="cotizaciones",
        db_column="id_entidad"
    )

    id_usuario_asesor = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name="cotizaciones_asesor",
        db_column="id_usuario_asesor"
    )

    precio_inmueble = models.DecimalField(max_digits=12, decimal_places=2)
    monto_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_inicial = models.DecimalField(max_digits=5, decimal_places=2)

    aplica_bono_techo_propio = models.BooleanField(null=True, blank=True)
    monto_bono_techo_propio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    monto_financiar = models.DecimalField(max_digits=12, decimal_places=2)

    MONEDA_CHOICES = [
        ('PEN', 'PEN'),
        ('USD', 'USD'),
    ]
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES)

    plazo_meses = models.IntegerField()

    tasa_interes = models.DecimalField(max_digits=8, decimal_places=6)

    TIPO_TASA_CHOICES = [
        ('nominal', 'Nominal'),
        ('efectiva', 'Efectiva'),
    ]
    tipo_tasa = models.CharField(max_length=10, choices=TIPO_TASA_CHOICES)

    CAPITALIZACION_CHOICES = [
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ]
    capitalizacion = models.CharField(max_length=10, choices=CAPITALIZACION_CHOICES, null=True, blank=True)

    tasa_efectiva_mensual = models.DecimalField(max_digits=8, decimal_places=6)
    tasa_efectiva_anual = models.DecimalField(max_digits=8, decimal_places=6)

    tiene_gracia = models.BooleanField(null=True, blank=True)

    TIPO_GRACIA_CHOICES = [
        ('total', 'Total'),
        ('parcial', 'Parcial'),
    ]
    tipo_gracia = models.CharField(max_length=10, choices=TIPO_GRACIA_CHOICES, null=True, blank=True)

    meses_gracia = models.IntegerField(null=True, blank=True)

    seguro_desgravamen = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    seguro_incendio = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    comision_apertura = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gastos_notariales = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gastos_registrales = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    cuota_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    cuota_con_seguros = models.DecimalField(max_digits=10, decimal_places=2)

    total_intereses = models.DecimalField(max_digits=12, decimal_places=2)
    total_pagar = models.DecimalField(max_digits=12, decimal_places=2)
    costo_total_credito = models.DecimalField(max_digits=12, decimal_places=2)

    tcea = models.DecimalField(max_digits=8, decimal_places=4)

    van_credito = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tir_credito = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    ratio_cuota_ingreso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    fecha_cotizacion = models.DateTimeField(null=True, blank=True)

    ESTADO_COT_CHOICES = [
        ('vigente', 'Vigente'),
        ('vencida', 'Vencida'),
        ('presentada_banco', 'Presentada a banco'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    estado_cotizacion = models.CharField(
        max_length=20,
        choices=ESTADO_COT_CHOICES,
        null=True,
        blank=True
    )

    class Meta:
        db_table = "cotizaciones_credito"

    def __str__(self):
        return self.codigo_cotizacion or f"Cotización {self.id_cotizacion}"
