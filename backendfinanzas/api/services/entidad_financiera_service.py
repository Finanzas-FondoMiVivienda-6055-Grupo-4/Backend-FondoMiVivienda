from api.repositories.entidad_financiera_repository import EntidadFinancieraRepository

class EntidadFinancieraService:

    @staticmethod
    def listar():
        return EntidadFinancieraRepository.list_all()

    @staticmethod
    def obtener(id_entidad: int):
        return EntidadFinancieraRepository.get_by_id(id_entidad)

    @staticmethod
    def registrar(data: dict):
        return EntidadFinancieraRepository.create(data)

    @staticmethod
    def actualizar(instance, data: dict):
        return EntidadFinancieraRepository.update(instance, data)

    @staticmethod
    def eliminar(instance):
        EntidadFinancieraRepository.delete(instance)
