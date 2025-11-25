from rest_framework import serializers
from api.models import UnidadInmobiliaria

class UnidadInmobiliariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadInmobiliaria
        fields = '__all__'
