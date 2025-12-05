from api.models import UnidadInmobiliaria

class UnidadInmobiliariaRepository:
    @staticmethod
    def list_all():
        return UnidadInmobiliaria.objects.all()

    @staticmethod
    def get_by_id(id_unidad: int):
        return UnidadInmobiliaria.objects.get(id_unidad=id_unidad)

    @staticmethod
    def create(data: dict):
        return UnidadInmobiliaria.objects.create(**data)

    @staticmethod
    def update(instance: UnidadInmobiliaria, data: dict):
        for k, v in data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

    @staticmethod
    def delete(instance: UnidadInmobiliaria):
        instance.delete()
    
    @staticmethod
    def list_by_proyecto(id_proyecto: int):
        return UnidadInmobiliaria.objects.filter(
            id_proyecto_id=id_proyecto
        )