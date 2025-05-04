from rest_framework import routers
from .api import PersonaViewSet, ClienteViewSet, AdministradorViewSet,DepartamentoViewSet,ReservaViewSet

router = routers.DefaultRouter()

router.register('api/persona', PersonaViewSet, 'persona')
router.register('api/cliente', ClienteViewSet, 'cliente')
router.register('api/administrador', AdministradorViewSet, 'administrador')
router.register('api/depto', DepartamentoViewSet, 'departamento')
router.register('api/reserva', ReservaViewSet, 'reserva')




urlpatterns = router.urls