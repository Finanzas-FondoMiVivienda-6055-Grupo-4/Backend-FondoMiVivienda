from django.db import models
from api.models import Usuario

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)

    TIPO_DOC_CHOICES = [
        ('DNI', 'DNI'),
        ('CE', 'CE'),
        ('PASAPORTE', 'PASAPORTE'),
    ]
    tipo_documento = models.CharField(max_length=15, choices=TIPO_DOC_CHOICES)

    numero_documento = models.CharField(max_length=20, null=True, blank=True)

    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)

    fecha_nacimiento = models.DateField()

    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    direccion = models.CharField(max_length=250)
    ocupacion = models.CharField(max_length=100)

    TIPO_EMPLEO_CHOICES = [
        ('dependiente', 'Dependiente'),
        ('independiente', 'Independiente'),
    ]
    tipo_empleo = models.CharField(max_length=20, choices=TIPO_EMPLEO_CHOICES)

    ingreso_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    gastos_mensuales = models.DecimalField(max_digits=10, decimal_places=2)

    deudas_actuales = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # FK hacia usuarios (id_usuario_registro)
    id_usuario_registro = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="clientes_registrados",
        db_column="id_usuario_registro"
    )

    fecha_registro = models.DateTimeField(null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "clientes"

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno}"
