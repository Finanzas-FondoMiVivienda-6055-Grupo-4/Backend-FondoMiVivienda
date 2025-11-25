from rest_framework import serializers
from api.models import CotizacionCredito

class CotizacionCreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CotizacionCredito
        fields = '__all__'
