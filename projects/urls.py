from rest_framework import routers
from .api import PersonaViewSet, ClienteViewSet, AdministradorViewSet

router = routers.DefaultRouter()

router.register('persona', PersonaViewSet, 'persona')
router.register('api/cliente', ClienteViewSet, 'cliente')
router.register('api/administrador', AdministradorViewSet, 'administrador')
    
urlpatterns = router.urls