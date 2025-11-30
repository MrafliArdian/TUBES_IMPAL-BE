from django.urls import path
from .views import KendaraanView

urlpatterns = [
    path("", KendaraanView.as_view(), name="simulasi-kendaraan"),
]
