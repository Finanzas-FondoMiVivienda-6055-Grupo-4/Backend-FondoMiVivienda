from rest_framework import viewsets
from api.models import Cliente
from api.api_layer.serializers import ClienteSerializer
from api.services.cliente_service import ClienteService

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()  # ✅ necesario para basename
    serializer_class = ClienteSerializer

    def get_queryset(self):
        return ClienteService.listar()

    def perform_create(self, serializer):
        data = serializer.validated_data

        # id_usuario viene dentro del token:
        id_usuario = self.request.auth.get("id_usuario")
        data["id_usuario_registro_id"] = id_usuario  # FK usando _id

        instance = ClienteService.registrar(data)
        serializer.instance = instance

    def perform_update(self, serializer):
        instance = ClienteService.actualizar(self.get_object(), serializer.validated_data)
        serializer.instance = instance

    def perform_destroy(self, instance):
        ClienteService.eliminar(instance)
