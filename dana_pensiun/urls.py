# dana_pensiun/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PensionViewSet

router = DefaultRouter()
router.register(r'', PensionViewSet, basename='dana-pensiun')

urlpatterns = [
    path('', include(router.urls)),
]
