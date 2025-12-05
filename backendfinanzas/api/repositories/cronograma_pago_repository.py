from api.models import CronogramaPago

class CronogramaPagoRepository:
    @staticmethod
    def list_all():
        return CronogramaPago.objects.all()

    @staticmethod
    def get_by_id(id_cronograma: int):
        return CronogramaPago.objects.get(id_cronograma=id_cronograma)

    @staticmethod
    def list_by_cotizacion(id_cotizacion: int):
        return CronogramaPago.objects.filter(
            id_cotizacion_id=id_cotizacion
        ).order_by('numero_cuota')

    @staticmethod
    def create(data: dict):
        return CronogramaPago.objects.create(**data)

    @staticmethod
    def update(instance: CronogramaPago, data: dict):
        for k, v in data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

    @staticmethod
    def delete(instance: CronogramaPago):
        instance.delete()
