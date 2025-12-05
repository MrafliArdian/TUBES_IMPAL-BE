<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import SimulasiKPRInputSerializer
from .models import SimulasiKPR

class SimulasiKPRView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SimulasiKPRInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Hitung DP dan pokok pinjaman
        uang_muka = data['harga_properti'] * (data['dp_percent']/100)
        pokok_pinjaman = data['harga_properti'] - uang_muka

        # Bunga per bulan
        bunga_fix_bulan = data['bunga_fix']/100 / 12
        bunga_floating_bulan = data['bunga_floating']/100 / 12

        # Total bunga periode fix
        total_bunga_fix = pokok_pinjaman * bunga_fix_bulan * data['periode_fix']

        # Sisa pokok setelah periode fix
        sisa_pokok_setelah_fix = pokok_pinjaman  # logika sederhana

        # Total bunga floating
        periode_floating = max(data['tenor_bulan'] - data['periode_fix'], 0)
        total_bunga_floating = sisa_pokok_setelah_fix * bunga_floating_bulan * periode_floating

        # Keterangan cukup / tidak cukup
        cicilan_bulanan_fix = (total_bunga_fix + pokok_pinjaman)/data['periode_fix'] if data['periode_fix'] > 0 else 0
        keterangan = "Cukup" if cicilan_bulanan_fix <= data['penghasilan'] else "Tidak cukup"

        # Simpan ke DB
        SimulasiKPR.objects.create(
            user=request.user,
            harga_properti=data['harga_properti'],
            penghasilan=data['penghasilan'],
            dp_percent=data['dp_percent'],
            tenor_bulan=data['tenor_bulan'],
            bunga_fix=data['bunga_fix'],
            periode_fix=data['periode_fix'],
            bunga_floating=data['bunga_floating'],
            pokok_pinjaman=pokok_pinjaman,
            total_bunga_fix=total_bunga_fix,
            total_bunga_floating=total_bunga_floating,
            sisa_pokok_setelah_fix=sisa_pokok_setelah_fix,
            keterangan=keterangan
        )

        return Response({
            "pokok_pinjaman": round(pokok_pinjaman),
            "total_bunga_fix": round(total_bunga_fix),
            "total_bunga_floating": round(total_bunga_floating),
            "sisa_pokok_setelah_fix": round(sisa_pokok_setelah_fix),
            "keterangan": keterangan
        })
>>>>>>> Dev_Nada
