from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importar ViewSets
from api.api_layer.views import (
    UsuarioViewSet, TareaViewSet,
    EntidadFinancieraViewSet, ClienteViewSet, CotizacionCreditoViewSet,
    ProyectoInmobiliarioViewSet, UnidadInmobiliariaViewSet,
    ConfiguracionViewSet, CronogramaPagoViewSet
)

# Importar Login personalizado (RUC + Contraseña)
from api.api_layer.auth.login_view import LoginRucView

# Router
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'tareas', TareaViewSet)
router.register(r'entidades-financieras', EntidadFinancieraViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'cotizaciones-credito', CotizacionCreditoViewSet)
router.register(r'proyectos-inmobiliarios', ProyectoInmobiliarioViewSet)
router.register(r'unidades-inmobiliarias', UnidadInmobiliariaViewSet)
router.register(r'configuracion', ConfiguracionViewSet)
router.register(r'cronograma-pagos', CronogramaPagoViewSet)

# URL patterns
urlpatterns = [
    
    path("auth/login/", LoginRucView.as_view(), name="login_ruc"),

    
    path("", include(router.urls)),
]
