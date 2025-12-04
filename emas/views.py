<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from rest_framework import viewsets, permissions
from .models import GoldCalculation
from .serializers import GoldCalculationSerializer


class GoldCalculationViewSet(viewsets.ModelViewSet):
    """
    Tujuan Endpoint:
    - GET    /api/emas/        → list riwayat emas user
    - POST   /api/emas/        → hitung baru
    - GET    /api/emas/{id}/   → detail
    - PUT/PATCH /api/emas/{id}/ → update + hitung ulang
    - DELETE /api/emas/{id}/   → hapus riwayat
    """

    serializer_class = GoldCalculationSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Untuk testing tanpa login:
    # permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return GoldCalculation.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
>>>>>>> 44da526b83f40d4dc6b1ef904768a5b18d335807
