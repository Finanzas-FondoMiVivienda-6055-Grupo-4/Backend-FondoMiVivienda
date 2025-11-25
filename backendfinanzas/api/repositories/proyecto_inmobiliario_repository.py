from api.models import ProyectoInmobiliario

class ProyectoInmobiliarioRepository:
    @staticmethod
    def list_all():
        return ProyectoInmobiliario.objects.all()

    @staticmethod
    def get_by_id(id_proyecto: int):
        return ProyectoInmobiliario.objects.get(id_proyecto=id_proyecto)

    @staticmethod
    def create(data: dict):
        return ProyectoInmobiliario.objects.create(**data)

    @staticmethod
    def update(instance: ProyectoInmobiliario, data: dict):
        for k, v in data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

    @staticmethod
    def delete(instance: ProyectoInmobiliario):
        instance.delete()
