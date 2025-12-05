<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializer import KendaraanInputSerializer

class KendaraanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = KendaraanInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        harga = data["harga_kendaraan"]
        dp_persen = data["dp_persen"] / 100
        uang_awal = data["uang_saat_ini"]
        bulanan = data["target_investasi_per_bulan"]
        return_inv = data["return_investasi"] / 100

        # Total uang yang harus dikumpulkan setelah DP
        total_butuh = harga - (harga * dp_persen)

        # Rumus sederhana future value 1 tahun pertama
        hasil_investasi = (uang_awal * (1 + return_inv)) + \
            (bulanan * ((1 + return_inv) - 1) / return_inv)

        status = "Cukup" if hasil_investasi >= total_butuh else "Tidak cukup"

        return Response({
            "total_uang_yang_dibutuhkan": round(total_butuh, 2),
            "hasil_investasi": round(hasil_investasi, 2),
            "status": status
        })
>>>>>>> Dev_Nada
