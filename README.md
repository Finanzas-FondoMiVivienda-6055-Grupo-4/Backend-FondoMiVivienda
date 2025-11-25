PROYECTO: BACKEND FONDO MIVIVIENDA
Este es el servidor Backend para la aplicacion de simulacion de creditos hipotecarios. Tecnologias: Django, Django REST Framework, PostgreSQL, Python.

REQUISITOS PREVIOS
Tener instalado Python (3.10 o superior).

Tener instalado PostgreSQL y haber creado una base de datos llamada "finanzas".

INSTALACION Y PUESTA EN MARCHA
PASO 1: Instalar dependencias Abre la terminal en la carpeta del proyecto y ejecuta: pip install -r requirements.txt

PASO 2: Configurar la Base de Datos

Ve al archivo: backendfinanzas/settings.py

Busca la seccion "DATABASES".

En el campo "PASSWORD", borra la contrasena actual y pon la tuya de PostgreSQL.

Guarda el archivo.

PASO 3: Crear las tablas (Migraciones) Ejecuta en la terminal: python manage.py makemigrations python manage.py migrate

PASO 4: Crear Usuario Administrador (Para Login) Ejecuta: python manage.py createsuperuser (Ingresa un RUC, correo y contrasena cuando te lo pida).

PASO 5: Iniciar el Servidor Ejecuta: python manage.py runserver

El servidor estara funcionando en: http://127.0.0.1:8000/

GUIA RAPIDA DE USO (ENDPOINTS)
LOGIN (Obtener Token)

URL: POST /api/auth/login/

Body (JSON): { "ruc": "TU_RUC", "password": "TU_PASSWORD" }

Respuesta: Recibiras un "access" token. Usalo en los Headers de las siguientes peticiones asi: Authorization: Bearer <tu_token_aqui>

CREAR SIMULACION (Cotizar)

URL: POST /api/cotizaciones-credito/

Header: Authorization: Bearer <tu_token_aqui>

Body (JSON Ejemplo): { "precio_inmueble": 120000.00, "monto_inicial": 12000.00, "aplica_bono_techo_propio": true, "plazo_meses": 120, "tasa_interes": 0.10, "tipo_tasa": "efectiva", "moneda": "PEN", "tipo_gracia": "total", "meses_gracia": 6, "id_cliente": 1, "id_entidad": 1, "id_usuario_asesor": 1, "id_unidad": 1, "cuota_mensual": 0, "total_intereses": 0, "total_pagar": 0, "costo_total_credito": 0, "tcea": 0, "tasa_efectiva_mensual": 0, "tasa_efectiva_anual": 0 }

NOTA: Los campos en 0 son calculados automaticamente por el sistema.
