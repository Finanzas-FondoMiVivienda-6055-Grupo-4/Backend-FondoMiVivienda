from rest_framework import viewsets
from api.models import UnidadInmobiliaria
from api.api_layer.serializers import UnidadInmobiliariaSerializer
from api.services.unidad_inmobiliaria_service import UnidadInmobiliariaService

class UnidadInmobiliariaViewSet(viewsets.ModelViewSet):
    queryset = UnidadInmobiliaria.objects.all()
    serializer_class = UnidadInmobiliariaSerializer

    def get_queryset(self):
        return UnidadInmobiliariaService.listar()

    def perform_create(self, serializer):
        instance = UnidadInmobiliariaService.registrar(serializer.validated_data)
        serializer.instance = instance

    def perform_update(self, serializer):
        instance = UnidadInmobiliariaService.actualizar(self.get_object(), serializer.validated_data)
        serializer.instance = instance

    def perform_destroy(self, instance):
        UnidadInmobiliariaService.eliminar(instance)
