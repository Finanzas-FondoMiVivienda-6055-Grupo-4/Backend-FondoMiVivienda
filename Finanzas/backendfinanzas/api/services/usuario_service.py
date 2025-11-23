from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from api.repositories.usuario_repository import UsuarioRepository

class UsuarioService:

    @staticmethod
    def listar():
        return UsuarioRepository.list_all()

    @staticmethod
    def obtener(id_usuario: int):
        return UsuarioRepository.get_by_id(id_usuario)

    @staticmethod
    def registrar(data: dict):
        """
        Espera que venga un campo 'password' en claro desde el request.
        Lo convierte a hash y lo guarda en password_hash.
        """
        password_plano = data.pop("password")
        data["password_hash"] = make_password(password_plano)
        data["fecha_creacion"] = timezone.now()
        data["estado"] = data.get("estado", "activo")

        return UsuarioRepository.create(data)

    @staticmethod
    def autenticar(ruc: str, password: str):
        usuario = UsuarioRepository.get_by_ruc(ruc)
        if not usuario:
            return None

        if not check_password(password, usuario.password_hash):
            return None

        usuario.ultimo_acceso = timezone.now()
        usuario.save(update_fields=["ultimo_acceso"])
        return usuario
