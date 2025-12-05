from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import CotizacionCredito
from api.api_layer.serializers import CotizacionCreditoSerializer, CronogramaPagoSerializer
from api.services.cotizacion_credito_service import CotizacionCreditoService
from api.services.cronograma_pago_service import CronogramaPagoService

class CotizacionCreditoViewSet(viewsets.ModelViewSet):
    queryset = CotizacionCredito.objects.all()
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

    # 🔹 Get cronogramas de pagos por id de cotizacion
    @action(detail=True, methods=['get'], url_path='cronograma')
    def cronograma(self, request, pk=None):
        """
        GET /cotizaciones-credito/{id}/cronograma/
        Devuelve el cronograma de pagos de esa cotización.
        """
        # pk es id_cotizacion
        cronograma_qs = CronogramaPagoService.listar_por_cotizacion(int(pk))
        serializer = CronogramaPagoSerializer(cronograma_qs, many=True)
        return Response(serializer.data)
