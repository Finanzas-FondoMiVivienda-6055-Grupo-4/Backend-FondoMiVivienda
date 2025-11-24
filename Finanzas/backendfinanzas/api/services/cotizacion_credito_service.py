from api.repositories.cotizacion_credito_repository import CotizacionCreditoRepository

class CotizacionCreditoService:

    @staticmethod
    def listar():
        return CotizacionCreditoRepository.list_all()

    @staticmethod
    def obtener(id_cotizacion: int):
        return CotizacionCreditoRepository.get_by_id(id_cotizacion)

    @staticmethod
    def registrar(data: dict):
        return CotizacionCreditoRepository.create(data)

    @staticmethod
    def actualizar(instance, data: dict):
        return CotizacionCreditoRepository.update(instance, data)

    @staticmethod
    def eliminar(instance):
        CotizacionCreditoRepository.delete(instance)
