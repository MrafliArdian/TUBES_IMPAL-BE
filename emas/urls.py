from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoldCalculationViewSet

router = DefaultRouter()
router.register(r'', GoldCalculationViewSet, basename='emas')

urlpatterns = [
    path('', include(router.urls)),
]
