from rest_framework import viewsets
from api.models import Configuracion
from api.api_layer.serializers import ConfiguracionSerializer
from api.services.configuracion_service import ConfiguracionService

class ConfiguracionViewSet(viewsets.ModelViewSet):
    queryset = Configuracion.objects.all()
    serializer_class = ConfiguracionSerializer

    def get_queryset(self):
        return ConfiguracionService.listar()

    def perform_create(self, serializer):
        instance = ConfiguracionService.registrar(serializer.validated_data)
        serializer.instance = instance

    def perform_update(self, serializer):
        instance = ConfiguracionService.actualizar(self.get_object(), serializer.validated_data)
        serializer.instance = instance

    def perform_destroy(self, instance):
        ConfiguracionService.eliminar(instance)
