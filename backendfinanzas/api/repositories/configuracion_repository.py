from api.models import Configuracion

class ConfiguracionRepository:
    @staticmethod
    def list_all():
        return Configuracion.objects.all()

    @staticmethod
    def get_by_id(id_config: int):
        return Configuracion.objects.get(id_config=id_config)

    @staticmethod
    def create(data: dict):
        return Configuracion.objects.create(**data)

    @staticmethod
    def update(instance: Configuracion, data: dict):
        for k, v in data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

    @staticmethod
    def delete(instance: Configuracion):
        instance.delete()
