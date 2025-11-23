from rest_framework import viewsets
from api.models import Usuario
from api.api_layer.serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
