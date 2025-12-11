# kendaraan/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleCalculationViewSet

router = DefaultRouter()
router.register(r'', VehicleCalculationViewSet, basename='kendaraan')

urlpatterns = [
    path('', include(router.urls)),
]
