# kendaraan/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .models import VehicleCalculation
from .serializers import VehicleCalculationSerializer


class VehicleCalculationViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk menghitung investasi kendaraan.
    
    Endpoint ini menghitung apakah dana yang terkumpul dari investasi
    bulanan cukup untuk membeli kendaraan setelah dikurangi DP.
    """
    serializer_class = VehicleCalculationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User hanya bisa melihat kalkulasi mereka sendiri
        return VehicleCalculation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ambil data input
        vehicle_price = serializer.validated_data['vehicle_price']
        down_payment = serializer.validated_data['down_payment']
        current_saving = serializer.validated_data['current_saving']
        monthly_invest = serializer.validated_data['monthly_invest']
        expected_return_pct = serializer.validated_data['expected_return_pct']
        investment_period_months = serializer.validated_data['investment_period_months']

        # Perhitungan
        needed_amount = vehicle_price - down_payment
        
        # Hitung future value dengan compound interest
        # FV = P(1+r)^n + PMT * [((1+r)^n - 1) / r]
        # P = current_saving, PMT = monthly_invest, r = monthly rate, n = months
        monthly_rate = (expected_return_pct / Decimal('100')) / Decimal('12')
        
        if monthly_rate > 0:
            # Compound interest formula
            growth_factor = (Decimal('1') + monthly_rate) ** investment_period_months
            
            # Future value dari tabungan awal
            fv_current = current_saving * growth_factor
            
            # Future value dari investasi bulanan (annuity)
            fv_monthly = monthly_invest * ((growth_factor - Decimal('1')) / monthly_rate)
            
            future_value = fv_current + fv_monthly
        else:
            # Jika return 0%, tidak ada bunga
            future_value = current_saving + (monthly_invest * investment_period_months)

        # Hitung gap
        gap_amount = future_value - needed_amount

        # Tentukan status
        if gap_amount >= 0:
            calc_status = "cukup"
            is_suitable = True
            recommendation = (
                f"Selamat! Dengan investasi Rp {monthly_invest:,.0f}/bulan selama "
                f"{investment_period_months} bulan dengan return {expected_return_pct}% per tahun, "
                f"Anda akan memiliki dana Rp {future_value:,.0f}. "
                f"Ini cukup untuk membeli kendaraan seharga Rp {vehicle_price:,.0f} "
                f"dengan DP Rp {down_payment:,.0f}. "
                f"Bahkan ada kelebihan dana sebesar Rp {gap_amount:,.0f}."
            )
        else:
            calc_status = "tidak cukup"
            is_suitable = False
            kekurangan = abs(gap_amount)
            additional_monthly = kekurangan / investment_period_months if investment_period_months > 0 else kekurangan
            recommendation = (
                f"Dana Anda masih kurang Rp {kekurangan:,.0f}. "
                f"Untuk mencapai target, Anda bisa: "
                f"1) Tambah investasi bulanan sekitar Rp {additional_monthly:,.0f}, atau "
                f"2) Perpanjang periode investasi, atau "
                f"3) Tingkatkan DP menjadi Rp {down_payment + kekurangan:,.0f}, atau "
                f"4) Cari kendaraan dengan harga lebih rendah."
            )

        # Simpan dengan hasil perhitungan
        serializer.save(
            user=self.request.user,
            needed_amount=needed_amount,
            future_value=future_value,
            gap_amount=gap_amount,
            status=calc_status,
            is_suitable=is_suitable,
            recommendation=recommendation
        )
