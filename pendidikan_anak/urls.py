# pendidikan_anak/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChildEducationCalculationViewSet

router = DefaultRouter()
router.register(r'', ChildEducationCalculationViewSet, basename='pendidikan-anak')

urlpatterns = [
    path('', include(router.urls)),
]
