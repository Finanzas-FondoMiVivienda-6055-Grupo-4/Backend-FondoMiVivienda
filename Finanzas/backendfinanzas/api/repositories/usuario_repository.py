from api.models import Usuario

class UsuarioRepository:

    @staticmethod
    def list_all():
        return Usuario.objects.all()

    @staticmethod
    def get_by_id(id_usuario: int):
        return Usuario.objects.get(id_usuario=id_usuario)

    @staticmethod
    def get_by_ruc(ruc: str):
        try:
            return Usuario.objects.get(ruc=ruc)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def create(data: dict):
        return Usuario.objects.create(**data)

    @staticmethod
    def update(instance: Usuario, data: dict):
        for k, v in data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

    @staticmethod
    def delete(instance: Usuario):
        instance.delete()
