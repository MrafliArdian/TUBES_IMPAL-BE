from django.urls import path
from .views import PendidikanAnakView

urlpatterns = [
    path("", PendidikanAnakView.as_view(), name="simulasi-pendidikan-anak"),
]
