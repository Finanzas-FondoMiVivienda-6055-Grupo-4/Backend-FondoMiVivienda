from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.models import Usuario
from api.api_layer.serializers import UsuarioSerializer
from api.services.usuario_service import UsuarioService


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        """
        - create (POST /api/usuarios/): público (registro de usuarios)
        - otros métodos (GET, PUT, DELETE): requieren autenticación
        """
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Sobreescribimos la creación para delegar en UsuarioService.registrar,
        que se encarga de:
        - hash de password
        - fecha_creacion
        - estado por defecto, etc.
        """
        instance = UsuarioService.registrar(serializer.validated_data)
        serializer.instance = instance
