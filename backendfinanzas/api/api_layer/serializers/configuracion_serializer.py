from rest_framework import serializers
from api.models import Configuracion

class ConfiguracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = '__all__'
