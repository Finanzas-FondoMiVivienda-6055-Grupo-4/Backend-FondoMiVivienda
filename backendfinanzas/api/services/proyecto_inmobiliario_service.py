from api.repositories.proyecto_inmobiliario_repository import ProyectoInmobiliarioRepository

class ProyectoInmobiliarioService:
    @staticmethod
    def listar():
        return ProyectoInmobiliarioRepository.list_all()

    @staticmethod
    def obtener(id_proyecto: int):
        return ProyectoInmobiliarioRepository.get_by_id(id_proyecto)

    @staticmethod
    def registrar(data: dict):
        return ProyectoInmobiliarioRepository.create(data)

    @staticmethod
    def actualizar(instance, data: dict):
        return ProyectoInmobiliarioRepository.update(instance, data)

    @staticmethod
    def eliminar(instance):
        ProyectoInmobiliarioRepository.delete(instance)
