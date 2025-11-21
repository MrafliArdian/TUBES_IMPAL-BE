from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

from rest_framework import viewsets, status
from .models import User
from .serializers import UserSerializer
        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Ambil data dari request
        data = request.data.copy()
        
        # Hash password sebelum diproses oleh serializer
        if 'password' in data:
            data['password'] = make_password(data['password'])
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_data = serializer.data.copy()
        return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def api_landing_page(request):
    """
    Menampilkan pintu gerbang/pesan sambutan API yang bersih.
    """
    return Response({
        'message': 'Selamat datang di Pintu Gerbang API Kalkulator Investasi!',
        'status': 'API Running',
        'auth_register_endpoint': '/api/v1/users/',
    })

def get_history_data(user_id):
    with connection.cursor() as cursor:
        # Contoh query untuk mengambil riwayat pengguna tertentu dari View
        cursor.execute(f"SELECT * FROM v_history WHERE user_id = {user_id} ORDER BY created_at DESC;")
        results = cursor.fetchall()
        return results