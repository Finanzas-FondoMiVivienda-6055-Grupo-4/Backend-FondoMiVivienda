PROYECTO: BACKEND FONDO MIVIVIENDA
Este es el servidor Backend para la aplicación de simulación de créditos hipotecarios.
Tecnologías: Django, Django REST Framework, PostgreSQL, Python.

REQUISITOS PREVIOS
– Tener instalado Python (3.10 o superior).
– Tener instalado PostgreSQL y haber creado una base de datos llamada "finanzas".
– (Optativo pero recomendado) Tener instalado pgAdmin para gestionar la base de datos.

INSTALACIÓN Y PUESTA EN MARCHA

PASO 1: Crear entorno virtual e instalar dependencias

Abre la terminal en la carpeta del proyecto donde se encuentra el archivo manage.py.

(Opcional pero recomendado) Crea y activa un entorno virtual:

Crear entorno virtual:
python -m venv venv

Activar entorno virtual en Windows:
venv\Scripts\activate

Instalar dependencias del proyecto:
pip install -r requirements.txt

PASO 2: Configurar la Base de Datos

Ve al archivo: backendfinanzas/settings.py

Busca la sección DATABASES.

En los campos "USER" y "PASSWORD", coloca tu usuario y contraseña reales de PostgreSQL. Por ejemplo:

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'finanzas',
'USER': 'postgres',
'PASSWORD': 'TU_PASSWORD',
'HOST': 'localhost',
'PORT': '5432',
}
}

Guarda el archivo.

PASO 3: Crear las tablas (Migraciones)

Ejecuta en la terminal (con el entorno virtual activado):

python manage.py migrate

Nota: No es necesario ejecutar "python manage.py makemigrations" a menos que se modifiquen los modelos del proyecto.

PASO 4: Crear Usuario para Login (IMPORTANTE)

El login de la API se hace por RUC y contraseña, usando el modelo Usuario.
No basta con crear un superusuario con "createsuperuser"; se debe crear un registro en la tabla Usuario.

Existen dos formas de contar con usuarios para probar la API:

Opción A: Crear usuario y datos de prueba automáticamente (seed_demo_data)

Ejecuta en la terminal:

python manage.py seed_demo_data

Este comando creará automáticamente:

– Un usuario asesor con RUC y contraseña.
– Un cliente de prueba.
– Una entidad financiera de prueba.
– Una unidad inmobiliaria de prueba.

Al finalizar verás en consola algo similar a:

=== LOGIN ===
POST /api/auth/login/
ruc: 12345678901
password: MiPassword123

=== IDs para crear cotización ===
id_cliente: 1
id_entidad: 1
id_usuario_asesor: 1
id_unidad: 1

Estos datos se pueden usar directamente en Postman o Swagger para autenticarse y crear cotizaciones.

Opción B: Registrar un usuario desde la API (POST /api/usuarios/)

El endpoint POST /api/usuarios/ permite registrar usuarios sin autenticación (registro público).
El cuerpo de la petición debe incluir el campo "password" en texto plano; el backend se encarga de convertirlo a "password_hash" y registrar la fecha de creación.

Body (JSON de ejemplo para registro):

{
"ruc": "151514848487",
"password": "comida123",
"nombre_completo": "testingregistrouserLogin",
"email": "user@example.com",
"estado": "activo",
"razon_social": "Usuario Demo"
}

Luego de registrar el usuario, podrás iniciar sesión en:

URL: POST /api/auth/login/

Body (JSON):

{
"ruc": "151514848487",
"password": "comida123"
}

La respuesta incluirá un campo "access" con el token JWT que deberás usar en los siguientes endpoints.

PASO 5: Iniciar el Servidor

Ejecuta en la terminal:
python manage.py runserver

El servidor estará funcionando en:
http://127.0.0.1:8000/

GUIA RÁPIDA DE USO (ENDPOINTS)

LOGIN (Obtener Token)

URL: POST /api/auth/login/

Body (JSON):

{
"ruc": "TU_RUC",
"password": "TU_PASSWORD"
}

Respuesta:
Recibirás un campo "access" (token JWT).
Úsalo en los headers de las siguientes peticiones así:

Authorization: Bearer <tu_token_aqui>

CREAR SIMULACIÓN (Cotizar)

URL: POST /api/cotizaciones-credito/

Header:
Authorization: Bearer <tu_token_aqui>
Content-Type: application/json

Body (JSON Ejemplo):

{
"id_unidad": 1,

"precio_inmueble": 120000.00,
"monto_inicial": 24000.00,
"porcentaje_inicial": 20.00,

"aplica_bono_techo_propio": true,
"monto_bono_techo_propio": 21400.00,

"monto_financiar": 74600.00,
"moneda": "PEN",
"plazo_meses": 120,

"tasa_interes": 0.10,
"tipo_tasa": "efectiva",
"capitalizacion": "mensual",

"tasa_efectiva_mensual": 0.007974,
"tasa_efectiva_anual": 0.100000,

"tiene_gracia": true,
"tipo_gracia": "total",
"meses_gracia": 6,

"seguro_desgravamen": 0.00,
"seguro_incendio": 0.00,
"comision_apertura": 0.00,
"gastos_notariales": 0.00,
"gastos_registrales": 0.00,

"cuota_mensual": 0,
"cuota_con_seguros": 0,
"total_intereses": 0,
"total_pagar": 0,
"costo_total_credito": 0,
"tcea": 0,

"id_cliente": 1,
"id_entidad": 1,
"id_usuario_asesor": 1
}

NOTA:
– Los campos enviados en 0 (como cuota_mensual, total_intereses, total_pagar, costo_total_credito, tcea, etc.) son calculados automáticamente por el sistema según las reglas financieras del crédito.
– Los IDs (id_cliente, id_entidad, id_usuario_asesor, id_unidad) pueden obtenerse fácilmente ejecutando el comando seed_demo_data o consultando previamente las entidades correspondientes.
