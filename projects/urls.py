from rest_framework import routers
from .api import PersonaViewSet, ClienteViewSet, AdministradorViewSet,DepartamentoViewSet,ReservaViewSet
from django.contrib import admin
from django.urls import path, include
from projects import views  # 👈 Importa tus vistas

router = routers.DefaultRouter()

router.register('api/persona', PersonaViewSet, 'persona')
router.register('api/cliente', ClienteViewSet, 'cliente')
router.register('api/administrador', AdministradorViewSet, 'administrador')
router.register('api/depto', DepartamentoViewSet, 'departamento')
router.register('api/reserva', ReservaViewSet, 'reserva')
router.register('api/addDepto', DepartamentoViewSet, 'add_depto')


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas del frontend (HTML)
    path('', views.index, name='index'),
    path('registro/', views.registerPage, name='registro'),
    path('administracion/', views.administracion, name='administracion'),
    path('eliminar_depto/<int:id>/', views.eliminar_depto, name='eliminar_depto'),
    path('transbank/inicio_pago/', views.iniciar_pago, name='iniciar_pago'),
    path('transbank/retorno/', views.confirm_pago, name='confirm_pago'),

    # Rutas de la API (REST framework)
    path('', include(router.urls)),

]
