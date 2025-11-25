from rest_framework import viewsets
from api.models import ProyectoInmobiliario
from api.api_layer.serializers import ProyectoInmobiliarioSerializer
from api.services.proyecto_inmobiliario_service import ProyectoInmobiliarioService

class ProyectoInmobiliarioViewSet(viewsets.ModelViewSet):
    queryset = ProyectoInmobiliario.objects.all()
    serializer_class = ProyectoInmobiliarioSerializer

    def get_queryset(self):
        return ProyectoInmobiliarioService.listar()

    def perform_create(self, serializer):
        instance = ProyectoInmobiliarioService.registrar(serializer.validated_data)
        serializer.instance = instance

    def perform_update(self, serializer):
        instance = ProyectoInmobiliarioService.actualizar(self.get_object(), serializer.validated_data)
        serializer.instance = instance

    def perform_destroy(self, instance):
        ProyectoInmobiliarioService.eliminar(instance)
