from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializer import PendidikanInputSerializer
from .models import PendidikanAnak

class PendidikanAnakView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PendidikanInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        usia_now = data["usia_anak_sekarang"]
        usia_kuliah = data["usia_masuk_kuliah"]
        biaya_tahunan = data["biaya_per_tahun"]
        lama_kuliah = data["lama_kuliah"]
        inflasi = data["inflasi_pendidikan"] / 100
        return_inv = data["return_investasi"] / 100

        # 1. Tahun menuju kuliah
        tahun_ke_kuliah = usia_kuliah - usia_now

        # 2. Hitung biaya kuliah tahun pertama
        biaya_mulai = biaya_tahunan * ((1 + inflasi) ** tahun_ke_kuliah)

        # 3. Total biaya seluruh tahun kuliah (inflasi tetap berjalan)
        total_biaya = 0
        biaya_tahun_ini = biaya_mulai

        for _ in range(lama_kuliah):
            total_biaya += biaya_tahun_ini
            biaya_tahun_ini *= (1 + inflasi)

        # 4. Berapa yang harus dipersiapkan sekarang (discount with return)
        dana_sekarang = total_biaya / ((1 + return_inv) ** tahun_ke_kuliah)

        # Save ke database
        obj = PendidikanAnak.objects.create(
            usia_anak_sekarang=usia_now,
            usia_masuk_kuliah=usia_kuliah,
            biaya_per_tahun=biaya_tahunan,
            lama_kuliah=lama_kuliah,
            inflasi_pendidikan=data["inflasi_pendidikan"],
            return_investasi=data["return_investasi"],
            total_biaya_kuliah_masa_depan=total_biaya,
            dana_yang_harus_dipersiapkan=dana_sekarang
        )

        return Response({
            "total_biaya_kuliah_masa_depan": round(total_biaya, 2),
            "dana_yang_harus_dipersiapkan": round(dana_sekarang, 2),
        })
