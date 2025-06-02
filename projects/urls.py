from rest_framework import routers
from .api import PersonaViewSet, ClienteViewSet, AdministradorViewSet,DepartamentoViewSet,ReservaViewSet
from django.contrib import admin
from django.urls import path, include
from .views import api_login
from projects import views  
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

router.register('api/persona', PersonaViewSet, 'persona')
router.register('api/cliente', ClienteViewSet, 'cliente')
router.register('api/administrador', AdministradorViewSet, 'administrador')
router.register('api/depto', DepartamentoViewSet, 'departamento')
router.register('api/reserva', ReservaViewSet, 'reserva')
router.register('api/addDepto', DepartamentoViewSet, 'add_depto')


urlpatterns = [   

    # HTML PAGES (Frontend)
    path('', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
    path('departamentos/', views.departamentos, name='departamentos'),
    
    # La ruta con ID debe ir antes que la genérica
    path('crear_reserva/<int:id_departamento>/', views.crear_reserva, name='crear_reserva'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),

    path('registro/', views.registerPage, name='registro'),
    path('login/', views.loginPage, name='login'),
    path('api/login/', api_login, name='api_login'),

   
    path('administracion/', views.administracion, name='administracion'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
   
    path('contacto/', views.contacto, name='contacto'),

    # Transbank
    path('pago/', views.iniciar_pago, name='iniciar_pago'),  # Para reserva temporal (vía session)
    path('transbank/retorno/', views.confirm_pago, name='confirm_pago'),

    # API (Django REST Framework)
    path('', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
