from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from .api import GastoViewSet, CategoriaViewSet, PresupuestoViewSet
from django.urls import path, include
router = routers.DefaultRouter()
# router.register('api/gastos', GastoViewSet)
# router.register('api/categorias', CategoriaViewSet)
router.register(r'gastos', GastoViewSet, 'gastos')
router.register(r'categorias', CategoriaViewSet, 'categorias')
router.register(r'presupuestos', PresupuestoViewSet, 'presupuestos')

# urlpatterns = router.urls
urlpatterns = [
    path("api/", include(router.urls)),
    path("docs/", include_docs_urls(title="Gastos API"))
]
