from api.models import EntidadFinanciera

class EntidadFinancieraRepository:

    @staticmethod
    def list_all():
        return EntidadFinanciera.objects.all()

    @staticmethod
    def get_by_id(id_entidad: int):
        return EntidadFinanciera.objects.get(id_entidad=id_entidad)

    @staticmethod
    def create(data: dict):
        return EntidadFinanciera.objects.create(**data)

    @staticmethod
    def update(instance: EntidadFinanciera, data: dict):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @staticmethod
    def delete(instance: EntidadFinanciera):
        instance.delete()
