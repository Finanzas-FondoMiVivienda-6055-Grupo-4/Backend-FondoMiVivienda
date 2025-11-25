from rest_framework import viewsets
from api.models import CotizacionCredito
from api.api_layer.serializers import CotizacionCreditoSerializer
from api.services.cotizacion_credito_service import CotizacionCreditoService

class CotizacionCreditoViewSet(viewsets.ModelViewSet):
    queryset = CotizacionCredito.objects.all()  # ✅ necesario para basename
    serializer_class = CotizacionCreditoSerializer

    def get_queryset(self):
        return CotizacionCreditoService.listar()

    def perform_create(self, serializer):
        instance = CotizacionCreditoService.registrar(serializer.validated_data)
        serializer.instance = instance

    def perform_update(self, serializer):
        instance = CotizacionCreditoService.actualizar(self.get_object(), serializer.validated_data)
        serializer.instance = instance

    def perform_destroy(self, instance):
        CotizacionCreditoService.eliminar(instance)
