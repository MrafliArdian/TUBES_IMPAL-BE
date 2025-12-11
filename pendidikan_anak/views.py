# pendidikan_anak/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .models import ChildEducationCalculation
from .serializers import ChildEducationCalculationSerializer


class ChildEducationCalculationViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk menghitung persiapan dana pendidikan anak.
    
    Endpoint ini menghitung apakah dana yang terkumpul dari investasi
    bulanan cukup untuk biaya kuliah dengan memperhitungkan inflasi pendidikan.
    """
    serializer_class = ChildEducationCalculationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User hanya bisa melihat kalkulasi mereka sendiri
        return ChildEducationCalculation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ambil data input
        child_age_years = serializer.validated_data['child_age_years']
        college_entry_age = serializer.validated_data['college_entry_age']
        current_tuition_per_year = serializer.validated_data['current_tuition_per_year']
        college_duration_years = serializer.validated_data['college_duration_years']
        education_inflation_pct = serializer.validated_data['education_inflation_pct']
        current_saving = serializer.validated_data['current_saving']
        monthly_invest = serializer.validated_data['monthly_invest']
        expected_return_pct = serializer.validated_data['expected_return_pct']

        # Perhitungan
        # 1. Hitung berapa tahun lagi sampai masuk kuliah
        years_until_college = int((college_entry_age - child_age_years) * 12) // 12  # dalam tahun penuh
        years_until_college_exact = college_entry_age - child_age_years
        
        # 2. Hitung biaya kuliah per tahun di masa depan dengan inflasi
        # Future Tuition = Current Tuition * (1 + inflation_rate)^years
        inflation_rate = education_inflation_pct / Decimal('100')
        future_tuition_per_year = current_tuition_per_year * ((Decimal('1') + inflation_rate) ** years_until_college_exact)
        
        # 3. Hitung total biaya kuliah (selama durasi kuliah)
        # Asumsi: inflasi tetap berlanjut selama masa kuliah
        total_education_need = Decimal('0')
        for year in range(college_duration_years):
            year_cost = future_tuition_per_year * ((Decimal('1') + inflation_rate) ** Decimal(year))
            total_education_need += year_cost
        
        # 4. Hitung future value dari investasi
        # FV = P(1+r)^n + PMT * [((1+r)^n - 1) / r]
        months_until_college = int(years_until_college_exact * 12)
        monthly_rate = (expected_return_pct / Decimal('100')) / Decimal('12')
        
        if monthly_rate > 0 and months_until_college > 0:
            # Compound interest formula
            growth_factor = (Decimal('1') + monthly_rate) ** months_until_college
            
            # Future value dari tabungan awal
            fv_current = current_saving * growth_factor
            
            # Future value dari investasi bulanan (annuity)
            fv_monthly = monthly_invest * ((growth_factor - Decimal('1')) / monthly_rate)
            
            future_value = fv_current + fv_monthly
        else:
            # Jika return 0% atau waktu 0
            future_value = current_saving + (monthly_invest * months_until_college)

        # 5. Hitung gap
        gap_amount = future_value - total_education_need

        # 6. Tentukan status dan rekomendasi
        if gap_amount >= 0:
            calc_status = "cukup"
            is_suitable = True
            recommendation = (
                f"Selamat! Dengan tabungan awal Rp {current_saving:,.0f} dan investasi "
                f"Rp {monthly_invest:,.0f}/bulan selama {years_until_college} tahun "
                f"(hingga anak berusia {college_entry_age} tahun) dengan return {expected_return_pct}% per tahun, "
                f"Anda akan memiliki dana Rp {future_value:,.0f}. "
                f"Ini sudah mencukupi untuk biaya kuliah total Rp {total_education_need:,.0f} "
                f"(biaya per tahun di masa depan: Rp {future_tuition_per_year:,.0f}, "
                f"selama {college_duration_years} tahun dengan inflasi {education_inflation_pct}% per tahun). "
                f"Bahkan ada kelebihan dana sebesar Rp {gap_amount:,.0f}."
            )
        else:
            calc_status = "tidak cukup"
            is_suitable = False
            kekurangan = abs(gap_amount)
            
            if months_until_college > 0:
                additional_monthly = kekurangan / months_until_college
            else:
                additional_monthly = kekurangan
            
            # Estimasi perpanjangan waktu jika tetap dengan investasi saat ini
            if monthly_invest > 0 and monthly_rate > 0:
                remaining_need = total_education_need - current_saving
                # Rough estimation
                estimated_months = int((remaining_need / monthly_invest) * Decimal('1.2'))
                additional_years = max(0, (estimated_months - months_until_college) // 12)
            else:
                additional_years = 0
            
            recommendation = (
                f"Dana Anda masih kurang Rp {kekurangan:,.0f}. "
                f"Total biaya kuliah yang dibutuhkan adalah Rp {total_education_need:,.0f} "
                f"(biaya per tahun saat anak kuliah: Rp {future_tuition_per_year:,.0f}). "
                f"Untuk mencapai target, Anda bisa: "
                f"1) Tambah investasi bulanan sekitar Rp {additional_monthly:,.0f}, atau "
                f"2) Mulai investasi lebih awal (anak Anda masih {child_age_years} tahun), atau "
                f"3) Cari beasiswa atau universitas dengan biaya lebih terjangkau, atau "
                f"4) Pertimbangkan instrumen investasi dengan return lebih tinggi (dengan risiko sesuai), atau "
                f"5) Kombinasi dari opsi di atas."
            )

        # Simpan dengan hasil perhitungan
        serializer.save(
            user=self.request.user,
            years_until_college=years_until_college,
            future_tuition_per_year=future_tuition_per_year,
            total_education_need=total_education_need,
            future_value=future_value,
            gap_amount=gap_amount,
            status=calc_status,
            is_suitable=is_suitable,
            recommendation=recommendation
        )
