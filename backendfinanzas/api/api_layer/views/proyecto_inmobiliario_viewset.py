from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import ProyectoInmobiliario
from api.api_layer.serializers import (
    ProyectoInmobiliarioSerializer,
    UnidadInmobiliariaSerializer,
)
from api.services.proyecto_inmobiliario_service import ProyectoInmobiliarioService
from api.services.unidad_inmobiliaria_service import UnidadInmobiliariaService

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

    # 🔹 ENDPOINT ESPECIAL
    @action(detail=True, methods=['get'], url_path='unidades')
    def unidades(self, request, pk=None):
        """
        GET /proyectos-inmobiliarios/{id}/unidades/
        Devuelve todas las unidades inmobiliarias del proyecto.
        """
        unidades_qs = UnidadInmobiliariaService.listar_por_proyecto(int(pk))
        serializer = UnidadInmobiliariaSerializer(unidades_qs, many=True)
        return Response(serializer.data)