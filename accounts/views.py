from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    UserDetailSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer
)
from .permissions import IsAdminUser

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User berhasil dibuat",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    """
    Endpoint untuk cek user yang sedang login.
    """
    return Response(UserSerializer(request.user).data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """
    Endpoint untuk user ganti password.
    POST /api/auth/change-password/
    
    Body:
    {
        "old_password": "current_password",
        "new_password": "new_password",
        "new_password2": "new_password"
    }
    """
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Password berhasil diubah",
            "detail": "Silakan login ulang dengan password baru"
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """
    Endpoint untuk update profile user.
    GET: Lihat profile
    PUT/PATCH: Update profile (email, full_name, phone_number)
    
    Note: Username TIDAK BISA diubah (read-only)
    """
    user = request.user
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    # PUT or PATCH
    serializer = UpdateProfileSerializer(
        user,
        data=request.data,
        partial=(request.method == 'PATCH')
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Profile berhasil diupdate",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =============================
# ADMIN ENDPOINTS
# =============================

@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_list_users(request):
    """
    Admin endpoint untuk melihat semua user yang terdaftar.
    GET /api/auth/admin/users/
    
    Query Parameters:
    - role: filter by role (USER/ADMIN)
    - search: search by username, email, atau full_name
    """
    users = User.objects.all()
    
    # Filter by role
    role = request.query_params.get('role', None)
    if role:
        users = users.filter(role=role)
    
    # Search functionality
    search = request.query_params.get('search', None)
    if search:
        from django.db.models import Q
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(full_name__icontains=search)
        )
    
    serializer = UserDetailSerializer(users, many=True)
    return Response({
        "count": users.count(),
        "users": serializer.data
    })


@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_user_detail(request, user_id):
    """
    Admin endpoint untuk melihat detail user tertentu.
    GET /api/auth/admin/users/<id>/
    """
    user = get_object_or_404(User, id=user_id)
    serializer = UserDetailSerializer(user)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_user_history(request, user_id):
    """
    Admin endpoint untuk melihat semua history perhitungan dari user tertentu.
    GET /api/auth/admin/users/<id>/history/
    
    Query Parameters:
    - calculator_type: filter by calculator type (emergency_fund, pension, gold, etc.)
    """
    user = get_object_or_404(User, id=user_id)
    
    history_data = {
        "user": UserSerializer(user).data,
        "calculations": {}
    }
    
    calculator_type = request.query_params.get('calculator_type', None)
    
    # Dana Darurat calculations
    if not calculator_type or calculator_type == 'emergency_fund':
        from dana_darurat.models import EmergencyFundCalculation
        from dana_darurat.serializers import EmergencyFundSerializer
        
        emergency_calcs = EmergencyFundCalculation.objects.filter(user=user)
        history_data["calculations"]["emergency_fund"] = EmergencyFundSerializer(emergency_calcs, many=True).data
    
    # Dana Pensiun calculations
    if not calculator_type or calculator_type == 'pension':
        from dana_pensiun.models import PensionCalculation
        from dana_pensiun.serializers import PensionSerializer
        
        pension_calcs = PensionCalculation.objects.filter(user=user)
        history_data["calculations"]["pension"] = PensionSerializer(pension_calcs, many=True).data
    
    # Gold calculations
    if not calculator_type or calculator_type == 'gold':
        from emas.models import GoldCalculation
        from emas.serializers import GoldCalculationSerializer
        
        gold_calcs = GoldCalculation.objects.filter(user=user)
        history_data["calculations"]["gold"] = GoldCalculationSerializer(gold_calcs, many=True).data
    
    return Response(history_data)
