from api.repositories.cliente_repository import ClienteRepository

class ClienteService:

    @staticmethod
    def listar():
        return ClienteRepository.list_all()

    @staticmethod
    def obtener(id_cliente: int):
        return ClienteRepository.get_by_id(id_cliente)

    @staticmethod
    def registrar(data: dict):
        return ClienteRepository.create(data)

    @staticmethod
    def actualizar(instance, data: dict):
        return ClienteRepository.update(instance, data)

    @staticmethod
    def eliminar(instance):
        ClienteRepository.delete(instance)
