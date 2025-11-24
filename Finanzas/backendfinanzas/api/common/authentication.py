from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import Usuario

class UsuarioJWTAuthentication(JWTAuthentication):
    """
    Autenticación JWT para tu modelo Usuario (tabla api_usuario).
    Lee id_usuario del token y setea request.user con ese Usuario.
    """

    def get_user(self, validated_token):
        id_usuario = validated_token.get("id_usuario")

        if not id_usuario:
            raise AuthenticationFailed(
                "Token sin id_usuario",
                code="token_not_valid"
            )

        try:
            return Usuario.objects.get(id_usuario=id_usuario)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed(
                "Usuario no existe",
                code="token_not_valid"
            )
