# artikel/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD:appKalku/urls.py

from .views import UserViewSet, api_landing_page
from .views import ValidateInvestmentStrategyView
=======
from .views import ArticleViewSet
>>>>>>> 44da526b83f40d4dc6b1ef904768a5b18d335807:artikel/urls.py

router = DefaultRouter()
router.register(r'', ArticleViewSet, basename='artikel')

urlpatterns = [
    path('', include(router.urls)),
    path('v1/validate-investment/', ValidateInvestmentStrategyView.as_view(), name='validate-investment'),
]
