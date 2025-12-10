from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView, 
    me, 
    change_password, 
    update_profile,
    admin_list_users, 
    admin_user_detail, 
    admin_user_history
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", me, name="auth_me"),
    
    # User profile management
    path("change-password/", change_password, name="change_password"),
    path("profile/", update_profile, name="update_profile"),
    
    # Admin endpoints
    path("admin/users/", admin_list_users, name="admin_list_users"),
    path("admin/users/<int:user_id>/", admin_user_detail, name="admin_user_detail"),
    path("admin/users/<int:user_id>/history/", admin_user_history, name="admin_user_history"),
]
