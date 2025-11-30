from rest_framework import serializers
from api.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    # Campo para que el cliente mande la contraseña en texto plano
    # Solo escritura (no se devuelve en la respuesta)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = [
            "id_usuario",
            "ruc",
            "password",        # <-- viene del request
            "nombre_completo",
            "email",
            "estado",
            "fecha_creacion",
            "ultimo_acceso",
            "razon_social",
        ]
        read_only_fields = ["id_usuario", "fecha_creacion", "ultimo_acceso"]
