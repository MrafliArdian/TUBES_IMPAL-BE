from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, api_landing_page
from .views import ValidateInvestmentStrategyView

router = DefaultRouter()
router.register(r'v1/users', UserViewSet, basename='user')

urlpatterns = [
    path('', api_landing_page, name='api-root'),
    path('', include(router.urls)),
    path('validate-strategy/', ValidateInvestmentStrategyView.as_view(), name='validate-strategy'),

]
