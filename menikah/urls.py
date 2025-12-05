from django.urls import path
from .views import MenikahView

urlpatterns = [
    path("", MenikahView.as_view(), name="simulasi-menikah"),
]
