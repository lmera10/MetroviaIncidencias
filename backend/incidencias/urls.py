from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncidenciaViewSet, CategoriaViewSet, CustomAuthToken

router = DefaultRouter()
router.register(r'incidencias', IncidenciaViewSet, basename='incidencia')
router.register(r'categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('', include(router.urls)),
]

