# menikah/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarriageCalculationViewSet

router = DefaultRouter()
router.register(r'', MarriageCalculationViewSet, basename='menikah')

urlpatterns = [
    path('', include(router.urls)),
]
