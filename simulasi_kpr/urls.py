# simulasi_kpr/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SimulasiKPRViewSet

router = DefaultRouter()
router.register(r'', SimulasiKPRViewSet, basename='simulasi-kpr')

urlpatterns = [
    path('', include(router.urls)),
]
