from api.repositories.configuracion_repository import ConfiguracionRepository

class ConfiguracionService:
    @staticmethod
    def listar():
        return ConfiguracionRepository.list_all()

    @staticmethod
    def obtener(id_config: int):
        return ConfiguracionRepository.get_by_id(id_config)

    @staticmethod
    def registrar(data: dict):
        return ConfiguracionRepository.create(data)

    @staticmethod
    def actualizar(instance, data: dict):
        return ConfiguracionRepository.update(instance, data)

    @staticmethod
    def eliminar(instance):
        ConfiguracionRepository.delete(instance)
