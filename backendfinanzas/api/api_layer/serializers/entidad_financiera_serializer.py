from rest_framework import serializers
from api.models import EntidadFinanciera

class EntidadFinancieraSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntidadFinanciera
        fields = '__all__'
