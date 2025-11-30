import logging

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Usuario

logger = logging.getLogger(__name__)


class AuthTests(APITestCase):
    """
    Tests del endpoint de login por RUC.

    Más que validar la lógica de negocio, estos tests sirven como
    herramienta de diagnóstico: dejan trazas de qué se envió,
    qué respondió la API y qué campo podría estar fallando.
    """

    @classmethod
    def setUpTestData(cls):
        # Credenciales solo para el entorno de tests (BD temporal)
        cls.ruc = "12345678901"
        cls.password_plano = "MiPassword123"

        logger.info("Creando usuario de prueba para login: ruc=%s", cls.ruc)

        Usuario.objects.create(
            ruc=cls.ruc,
            password_hash=make_password(cls.password_plano),
            nombre_completo="Usuario de Prueba",
            email="test@example.com",
            estado="activo",
        )

    def test_login_correcto_devuelve_token(self):
        """
        Caso feliz: el login debería devolver status 200 y un campo 'access'.
        Si falla, el mensaje del assert mostrará el status y el response.data.
        """
        url = "/api/auth/login/"
        payload = {
            "ruc": self.ruc,
            "password": self.password_plano,
        }

        logger.info("[LOGIN OK] Enviando POST %s con payload=%s", url, payload)
        response = self.client.post(url, payload, format="json")

        if response.status_code != status.HTTP_200_OK:
            logger.error(
                "[LOGIN OK] Falló. status=%s, response=%s",
                response.status_code,
                response.data,
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"[LOGIN OK] Esperado 200, obtenido {response.status_code}. "
                f"Response: {response.data}",
        )

        self.assertIn(
            "access",
            response.data,
            msg=f"[LOGIN OK] No se encontró el campo 'access' en la respuesta. "
                f"Response: {response.data}",
        )

        token = response.data["access"]
        logger.info("[LOGIN OK] Token obtenido (len=%d)", len(token))
        self.assertTrue(token, msg="[LOGIN OK] El token 'access' está vacío.")

    def test_login_credenciales_invalidas(self):
        """
        Caso de contraseña incorrecta:
        Debería devolver 401. Si devuelve otra cosa, lo reporta con detalle.
        """
        url = "/api/auth/login/"
        payload = {
            "ruc": self.ruc,
            "password": "clave_incorrecta",
        }

        logger.info("[LOGIN BAD_PASSWORD] Enviando POST %s con payload=%s", url, payload)
        response = self.client.post(url, payload, format="json")

        logger.info(
            "[LOGIN BAD_PASSWORD] status=%s, response=%s",
            response.status_code,
            response.data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=(
                "[LOGIN BAD_PASSWORD] Se esperaba 401 para credenciales inválidas, "
                f"pero se obtuvo {response.status_code}. Response: {response.data}"
            ),
        )

    def test_login_body_incompleto(self):
        """
        Caso de body incompleto (falta password).
        Útil para detectar validaciones de serializer o request.data.
        """
        url = "/api/auth/login/"
        payload = {
            "ruc": self.ruc,
            # "password" ausente intencionalmente
        }

        logger.info("[LOGIN INCOMPLETO] Enviando POST %s con payload=%s", url, payload)
        response = self.client.post(url, payload, format="json")

        logger.info(
            "[LOGIN INCOMPLETO] status=%s, response=%s",
            response.status_code,
            response.data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg=(
                "[LOGIN INCOMPLETO] Se esperaba 400 por body incompleto, "
                f"pero se obtuvo {response.status_code}. Response: {response.data}"
            ),
        )
