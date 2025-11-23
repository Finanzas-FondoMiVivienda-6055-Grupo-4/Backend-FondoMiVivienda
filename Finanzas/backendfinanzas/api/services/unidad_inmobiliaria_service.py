from api.repositories.unidad_inmobiliaria_repository import UnidadInmobiliariaRepository

class UnidadInmobiliariaService:
    @staticmethod
    def listar():
        return UnidadInmobiliariaRepository.list_all()

    @staticmethod
    def obtener(id_unidad: int):
        return UnidadInmobiliariaRepository.get_by_id(id_unidad)

    @staticmethod
    def registrar(data: dict):
        return UnidadInmobiliariaRepository.create(data)

    @staticmethod
    def actualizar(instance, data: dict):
        return UnidadInmobiliariaRepository.update(instance, data)

    @staticmethod
    def eliminar(instance):
        UnidadInmobiliariaRepository.delete(instance)
