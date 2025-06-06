from rest_framework import routers
from .api import PersonaViewSet, ClienteViewSet, AdministradorViewSet,DepartamentoViewSet,ReservaViewSet,ContactoViewSet, RolViewSet
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
router.register('api/contacto', ContactoViewSet, 'contacto')
router.register('api/rol', RolViewSet, 'rol')


urlpatterns = [   

    # HTML PAGES (Frontend)
    path('', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
    path('departamentos/', views.departamentos, name='departamentos'),
    path('profile/', views.profile, name='profile'),
    #logout
    path('logout/', views.logout, name='logout'),
    
    # La ruta con ID debe ir antes que la genérica
    path('crear_reserva/<int:departamento>/', views.crear_reserva, name='crear_reserva'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),

    path('guardar_reserva/', views.guardar_reserva, name='guardar_reserva'),

    path('registro/', views.registerPage, name='registro'),
    path('login/', views.loginPage, name='login'),
    path('api/login/', api_login, name='api_login'),        
    
    path('administracion/', views.administracion, name='administracion'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
   
    path('contacto/', views.contacto, name='contacto'),

    # Transbank
    path('transbank/inicio_pago/<int:id_reserva>/', views.iniciar_pago, name='inicio_pago'),
    path('transbank/retorno/', views.confirm_pago, name='confirm_pago'),

    # API (Django REST Framework)
    path('', include(router.urls)),
    
    #reserva AJAX    
    path('api/crear_reserva_ajax/', views.crear_reserva_ajax, name='crear_reserva_ajax'),
    
    # validar reservas    
    path('validar_reserva/', views.validar_reserva, name='validar_reserva'),

    
    #API paises de rapidAPI geocities
    # path('api/paises/', views.get_paises, name='get_paises'),
    # path('api/ciudades/', views.get_ciudades, name='get_ciudades'),
    
    # # API para obtener la clave de RapidAPI
    # path('api/get-rapidapi-key/', get_rapidapi_key, name='get_rapidapi_key'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
