from api.repositories.cronograma_pago_repository import CronogramaPagoRepository

class CronogramaPagoService:
    @staticmethod
    def listar():
        return CronogramaPagoRepository.list_all()

    @staticmethod
    def obtener(id_cronograma: int):
        return CronogramaPagoRepository.get_by_id(id_cronograma)

    @staticmethod
    def registrar(data: dict):
        return CronogramaPagoRepository.create(data)

    @staticmethod
    def actualizar(instance, data: dict):
        return CronogramaPagoRepository.update(instance, data)

    @staticmethod
    def eliminar(instance):
        CronogramaPagoRepository.delete(instance)
