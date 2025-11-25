from rest_framework import viewsets
from api.models import CronogramaPago
from api.api_layer.serializers import CronogramaPagoSerializer
from api.services.cronograma_pago_service import CronogramaPagoService

class CronogramaPagoViewSet(viewsets.ModelViewSet):
    queryset = CronogramaPago.objects.all()
    serializer_class = CronogramaPagoSerializer

    def get_queryset(self):
        return CronogramaPagoService.listar()

    def perform_create(self, serializer):
        instance = CronogramaPagoService.registrar(serializer.validated_data)
        serializer.instance = instance

    def perform_update(self, serializer):
        instance = CronogramaPagoService.actualizar(self.get_object(), serializer.validated_data)
        serializer.instance = instance

    def perform_destroy(self, instance):
        CronogramaPagoService.eliminar(instance)
