from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from api.models import (
    Usuario,
    Cliente,
    EntidadFinanciera,
    ProyectoInmobiliario,
    UnidadInmobiliaria
)


class Command(BaseCommand):
    help = "Crea datos de demostración para probar la API Fondo MiVivienda usando Postman."

    def handle(self, *args, **options):

        self.stdout.write("⏳ Creando datos de demostración...\n")

        # ----------------------------------------------------
        # 1) Usuario asesor (login por RUC)
        # ----------------------------------------------------
        ruc_demo = "12345678901"
        password_demo = "MiPassword123"

        usuario, created_usuario = Usuario.objects.get_or_create(
            ruc=ruc_demo,
            defaults={
                "password_hash": make_password(password_demo),
                "nombre_completo": "Asesor Demo",
                "email": "asesor.demo@example.com",
                "estado": "activo",
            },
        )

        # ----------------------------------------------------
        # 2) Entidad financiera demo
        # ----------------------------------------------------
        entidad, created_entidad = EntidadFinanciera.objects.get_or_create(
            nombre="Banco Demo",
            defaults={
                "tasa_min": 0.05,
                "tasa_max": 0.12,
                "plazo_min_meses": 12,
                "plazo_max_meses": 240,
                "permite_gracia": True,
                "estado": "activo",
            }
        )

        # ----------------------------------------------------
        # 3) Proyecto inmobiliario demo
        # ----------------------------------------------------
        proyecto, created_proyecto = ProyectoInmobiliario.objects.get_or_create(
            nombre_proyecto="Residencial Demo",
            defaults={
                "ubicacion": "Av. Primavera 123",
                "distrito": "Chiclayo",
                "estado": "activo",
            }
        )

        # ----------------------------------------------------
        # 4) Unidad inmobiliaria demo
        # ----------------------------------------------------
        unidad, created_unidad = UnidadInmobiliaria.objects.get_or_create(
            codigo_unidad="U101",
            id_proyecto=proyecto,
            defaults={
                "tipo_unidad": "departamento",
                "area_construida": 75.00,
                "area_total": 82.00,
                "num_dormitorios": 3,
                "num_banos": 2,
                "num_estacionamientos": 1,
                "precio_venta": 120000.00,
                "moneda_precio": "PEN",
                "inicial_minima_porc": 10.00,
                "elegible_bono_techo_propio": True,
                "estado": "disponible",
            }
        )

        # ----------------------------------------------------
        # 5) Cliente demo
        # ----------------------------------------------------
        cliente, created_cliente = Cliente.objects.get_or_create(
            numero_documento="12345678",
            defaults={
                "tipo_documento": "DNI",
                "nombres": "Juan",
                "apellido_paterno": "Pérez",
                "apellido_materno": "Gómez",
                "fecha_nacimiento": "1990-01-01",
                "telefono": "999999999",
                "email": "cliente.demo@example.com",
                "direccion": "Av. Siempre Viva 123",
                "ocupacion": "Empleado",
                "tipo_empleo": "dependiente",
                "ingreso_mensual": 3000.00,
                "gastos_mensuales": 1000.00,
                "deudas_actuales": 0.00,
                "id_usuario_registro": usuario,
            }
        )

        # ----------------------------------------------------
        # Imprimir información final
        # ----------------------------------------------------
        self.stdout.write(self.style.SUCCESS("\n✅ Datos de demostración creados correctamente.\n"))
        self.stdout.write("👉 Usa estos datos en Postman:\n")

        self.stdout.write("=== LOGIN ===")
        self.stdout.write("POST /api/auth/login/")
        self.stdout.write(f"  ruc: {ruc_demo}")
        self.stdout.write(f"  password: {password_demo}\n")

        self.stdout.write("=== IDs para crear cotización ===")
        self.stdout.write(f"  id_cliente: {cliente.id_cliente}")
        self.stdout.write(f"  id_entidad: {entidad.id_entidad}")
        self.stdout.write(f"  id_usuario_asesor: {usuario.id_usuario}")
        self.stdout.write(f"  id_unidad: {unidad.id_unidad}\n")

        self.stdout.write(self.style.WARNING("⚠ Importante: Ajusta los valores según tu flujo lógico."))
