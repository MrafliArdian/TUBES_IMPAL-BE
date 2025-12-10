# history/urls.py
from django.urls import path
from .views import unified_history, calculator_history

urlpatterns = [
    path('', unified_history, name='unified_history'),
    path('<str:calculator_type>/', calculator_history, name='calculator_history'),
]
