from api.models import CotizacionCredito

class CotizacionCreditoRepository:

    @staticmethod
    def list_all():
        return CotizacionCredito.objects.all()

    @staticmethod
    def get_by_id(id_cotizacion: int):
        return CotizacionCredito.objects.get(id_cotizacion=id_cotizacion)

    @staticmethod
    def create(data: dict):
        return CotizacionCredito.objects.create(**data)

    @staticmethod
    def update(instance: CotizacionCredito, data: dict):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @staticmethod
    def delete(instance: CotizacionCredito):
        instance.delete()
