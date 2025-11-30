from django.urls import path
from .views import SimulasiKPRView

urlpatterns = [
    path("", SimulasiKPRView.as_view(), name="simulasi-kpr"),
]
