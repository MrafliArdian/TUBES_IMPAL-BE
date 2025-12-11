# menikah/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .models import MarriageCalculation
from .serializers import MarriageCalculationSerializer


class MarriageCalculationViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk menghitung persiapan dana pernikahan.
    
    Endpoint ini menghitung apakah dana yang terkumpul dari tabungan
    dan investasi bulanan cukup untuk biaya pernikahan target.
    """
    serializer_class = MarriageCalculationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User hanya bisa melihat kalkulasi mereka sendiri
        return MarriageCalculation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ambil data input
        target_cost = serializer.validated_data['target_cost']
        current_saving = serializer.validated_data['current_saving']
        months_to_event = serializer.validated_data['months_to_event']
        monthly_invest = serializer.validated_data['monthly_invest']
        expected_return_pct = serializer.validated_data['expected_return_pct']

        # Perhitungan Future Value
        # FV = P(1+r)^n + PMT * [((1+r)^n - 1) / r]
        monthly_rate = (expected_return_pct / Decimal('100')) / Decimal('12')
        
        if monthly_rate > 0:
            # Compound interest formula
            growth_factor = (Decimal('1') + monthly_rate) ** months_to_event
            
            # Future value dari tabungan awal
            fv_current = current_saving * growth_factor
            
            # Future value dari investasi bulanan (annuity)
            fv_monthly = monthly_invest * ((growth_factor - Decimal('1')) / monthly_rate)
            
            future_value = fv_current + fv_monthly
        else:
            # Jika return 0%, tidak ada bunga
            future_value = current_saving + (monthly_invest * months_to_event)

        # Hitung gap
        gap_amount = future_value - target_cost

        # Tentukan status dan rekomendasi
        if gap_amount >= 0:
            calc_status = "cukup"
            is_suitable = True
            recommendation = (
                f"Selamat! Dengan tabungan awal Rp {current_saving:,.0f} dan investasi "
                f"Rp {monthly_invest:,.0f}/bulan selama {months_to_event} bulan "
                f"dengan return {expected_return_pct}% per tahun, "
                f"Anda akan memiliki dana Rp {future_value:,.0f}. "
                f"Ini sudah mencukupi untuk biaya pernikahan target Rp {target_cost:,.0f}. "
                f"Bahkan ada kelebihan dana sebesar Rp {gap_amount:,.0f} untuk keperluan lain."
            )
        else:
            calc_status = "tidak cukup"
            is_suitable = False
            kekurangan = abs(gap_amount)
            additional_monthly = kekurangan / months_to_event if months_to_event > 0 else kekurangan
            
            # Hitung berapa bulan lagi yang dibutuhkan dengan investasi saat ini
            if monthly_invest > 0 and monthly_rate > 0:
                remaining_need = target_cost - current_saving
                # Solve for n: remaining_need = PMT * [((1+r)^n - 1) / r]
                # Simplified estimation
                additional_months = int((remaining_need / monthly_invest) * Decimal('1.1'))  # rough estimate
            else:
                additional_months = 0
            
            recommendation = (
                f"Dana Anda masih kurang Rp {kekurangan:,.0f}. "
                f"Untuk mencapai target pernikahan, Anda bisa: "
                f"1) Tambah investasi bulanan sekitar Rp {additional_monthly:,.0f}, atau "
                f"2) Perpanjang waktu persiapan sekitar {additional_months} bulan lagi, atau "
                f"3) Kurangi budget pernikahan menjadi sekitar Rp {future_value:,.0f}, atau "
                f"4) Kombinasi dari opsi di atas."
            )

        # Simpan dengan hasil perhitungan
        serializer.save(
            user=self.request.user,
            future_value=future_value,
            gap_amount=gap_amount,
            status=calc_status,
            is_suitable=is_suitable,
            recommendation=recommendation
        )
