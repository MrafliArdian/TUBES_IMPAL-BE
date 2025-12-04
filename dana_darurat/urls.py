# dana_darurat/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmergencyFundViewSet

router = DefaultRouter()
router.register(r'', EmergencyFundViewSet, basename='dana-darurat')

urlpatterns = [
    path('', include(router.urls)),
]
