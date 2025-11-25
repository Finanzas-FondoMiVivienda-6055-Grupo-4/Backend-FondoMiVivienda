from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from api.services.usuario_service import UsuarioService

class LoginRucView(APIView):
    permission_classes = []

    def post(self, request):
        ruc = request.data.get("ruc")
        password = request.data.get("password")

        if not ruc or not password:
            return Response(
                {"detail": "RUC y password son requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario = UsuarioService.autenticar(ruc, password)
        if not usuario:
            return Response(
                {"detail": "Credenciales inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Refresh token
        refresh = RefreshToken()
        refresh["id_usuario"] = usuario.id_usuario
        refresh["ruc"] = usuario.ruc
        refresh["nombre_completo"] = usuario.nombre_completo

        # Access token directo
        access = AccessToken()
        access["id_usuario"] = usuario.id_usuario
        access["ruc"] = usuario.ruc
        access["nombre_completo"] = usuario.nombre_completo

        return Response({
            "refresh": str(refresh),
            "access": str(access),
            "usuario": {
                "id_usuario": usuario.id_usuario,
                "ruc": usuario.ruc,
                "nombre_completo": usuario.nombre_completo,
                "email": usuario.email
            }
        })
