from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializer import MenikahInputSerializer
from .models import SimulasiMenikah


class MenikahView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MenikahInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Ambil input
        target = data["target_biaya_menikah"]
        uang_awal = data["uang_saat_ini"]
        bulanan = data["target_investasi_per_bulan"]
        return_investasi = data["return_investasi"] / 100  
        tahun_target = data["target_usia_menikah"]

        lama_investasi = tahun_target 

        # Rumus future value (FV)
        hasil_investasi = uang_awal * (1 + return_investasi)**lama_investasi + \
            bulanan * (((1 + return_investasi)**lama_investasi - 1) / return_investasi)

        # Cek cukup/tidak
        status = "Cukup" if hasil_investasi >= target else "Tidak cukup"

        # 🔥 SIMPAN KE DATABASE 🔥
        SimulasiMenikah.objects.create(
            user=request.user,
            target_biaya_menikah=target,
            uang_saat_ini=uang_awal,
            target_investasi_per_bulan=bulanan,
            return_investasi=data["return_investasi"],
            target_usia_menikah=tahun_target,
            hasil_investasi=hasil_investasi,
            status=status,
        )

        # Return ke FE
        return Response({
            "total_biaya": target,
            "hasil_investasi": round(hasil_investasi, 2),
            "status": status
        })
