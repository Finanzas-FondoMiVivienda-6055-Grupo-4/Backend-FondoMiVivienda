from rest_framework import viewsets
from api.models import EntidadFinanciera
from api.api_layer.serializers import EntidadFinancieraSerializer
from api.services.entidad_financiera_service import EntidadFinancieraService

class EntidadFinancieraViewSet(viewsets.ModelViewSet):
    queryset = EntidadFinanciera.objects.all()  
    serializer_class = EntidadFinancieraSerializer

    def get_queryset(self):
        return EntidadFinancieraService.listar()

    def perform_create(self, serializer):
        instance = EntidadFinancieraService.registrar(serializer.validated_data)
        serializer.instance = instance  

    def perform_update(self, serializer):
        instance = EntidadFinancieraService.actualizar(self.get_object(), serializer.validated_data)
        serializer.instance = instance  

    def perform_destroy(self, instance):
        EntidadFinancieraService.eliminar(instance)
