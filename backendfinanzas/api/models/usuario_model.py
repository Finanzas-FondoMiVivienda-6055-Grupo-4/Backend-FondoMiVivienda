from django.db import models


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    ruc = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255)
    nombre_completo = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)

    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, null=True, blank=True)

    fecha_creacion = models.DateTimeField(null=True, blank=True)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    razon_social = models.CharField(max_length=50)

    def __str__(self):
        return str(self.nombre_completo)

    # =====================================================
    # 🔐 Necesario para que DRF acepte este usuario como autenticado
    # =====================================================

    @property
    def is_authenticated(self):
        """
        DRF y Django usan esto para saber si el usuario está autenticado.
        Como nuestro modelo no hereda de AbstractBaseUser, debemos declararlo.
        Siempre será True porque si llegamos aquí, el token ya validó.
        """
        return True

    @property
    def is_anonymous(self):
        """
        El usuario nunca es "anónimo" si existe instancia.
        """
        return False
