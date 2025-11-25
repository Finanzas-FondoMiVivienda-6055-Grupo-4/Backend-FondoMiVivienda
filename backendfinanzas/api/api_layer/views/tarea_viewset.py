from rest_framework import viewsets
from api.models import Tarea
from api.api_layer.serializers import TareaSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
