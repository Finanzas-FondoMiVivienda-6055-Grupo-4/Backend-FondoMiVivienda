from rest_framework import serializers
from api.models import CronogramaPago

class CronogramaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CronogramaPago
        fields = '__all__'
