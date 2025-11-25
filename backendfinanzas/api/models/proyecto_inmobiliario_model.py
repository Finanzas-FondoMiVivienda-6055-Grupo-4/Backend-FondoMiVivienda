from django.db import models

class ProyectoInmobiliario(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre_proyecto = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=250)
    distrito = models.CharField(max_length=100)

    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, null=True, blank=True)

    fecha_creacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "proyectos_inmobiliarios"

    def __str__(self):
        return self.nombre_proyecto
