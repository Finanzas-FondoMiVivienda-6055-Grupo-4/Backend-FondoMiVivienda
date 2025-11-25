from api.models import Cliente

class ClienteRepository:

    @staticmethod
    def list_all():
        return Cliente.objects.all()

    @staticmethod
    def get_by_id(id_cliente: int):
        return Cliente.objects.get(id_cliente=id_cliente)

    @staticmethod
    def create(data: dict):
        return Cliente.objects.create(**data)

    @staticmethod
    def update(instance: Cliente, data: dict):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @staticmethod
    def delete(instance: Cliente):
        instance.delete()
