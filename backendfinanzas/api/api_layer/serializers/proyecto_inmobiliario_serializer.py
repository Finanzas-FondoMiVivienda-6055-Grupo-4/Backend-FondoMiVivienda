from rest_framework import serializers
from api.models import ProyectoInmobiliario

class ProyectoInmobiliarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoInmobiliario
        fields = '__all__'
