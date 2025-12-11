# simulasi_kpr/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .models import SimulasiKPR
from .serializer import SimulasiKPRSerializer


class SimulasiKPRViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk simulasi KPR (Kredit Pemilikan Rumah).
    
    Endpoint ini menghitung cicilan KPR dengan bunga fixed dan floating,
    serta menentukan apakah KPR affordable berdasarkan rasio cicilan terhadap pendapatan.
    """
    serializer_class = SimulasiKPRSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User hanya bisa melihat simulasi mereka sendiri
        return SimulasiKPR.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ambil data input
        property_price = serializer.validated_data['property_price']
        monthly_income = serializer.validated_data['monthly_income']
        dp_percentage = serializer.validated_data['dp_percentage']
        loan_term_months = serializer.validated_data['loan_term_months']
        fixed_interest_rate = serializer.validated_data['fixed_interest_rate']
        fixed_period_months = serializer.validated_data['fixed_period_months']
        floating_interest_rate = serializer.validated_data['floating_interest_rate']

        # Perhitungan DP dan Loan Amount
        dp_amount = property_price * (dp_percentage / Decimal('100'))
        loan_amount = property_price - dp_amount

        # Hitung cicilan dengan bunga fixed
        # Formula: PMT = P * [r(1+r)^n] / [(1+r)^n - 1]
        # P = loan amount, r = monthly rate, n = number of months
        monthly_fixed_rate = (fixed_interest_rate / Decimal('100')) / Decimal('12')
        
        if monthly_fixed_rate > 0:
            growth_factor_fixed = (Decimal('1') + monthly_fixed_rate) ** loan_term_months
            monthly_installment_fixed = loan_amount * (
                (monthly_fixed_rate * growth_factor_fixed) / (growth_factor_fixed - Decimal('1'))
            )
        else:
            # Jika bunga 0%
            monthly_installment_fixed = loan_amount / loan_term_months

        # Hitung cicilan dengan bunga floating
        monthly_floating_rate = (floating_interest_rate / Decimal('100')) / Decimal('12')
        
        if monthly_floating_rate > 0:
            growth_factor_floating = (Decimal('1') + monthly_floating_rate) ** loan_term_months
            monthly_installment_floating = loan_amount * (
                (monthly_floating_rate * growth_factor_floating) / (growth_factor_floating - Decimal('1'))
            )
        else:
            # Jika bunga 0%
            monthly_installment_floating = loan_amount / loan_term_months

        # Untuk analisis, gunakan cicilan floating (worst case setelah periode fixed)
        # atau bisa juga pakai rata-rata weighted
        # Untuk simplicity, kita pakai floating rate sebagai acuan
        installment_for_ratio = monthly_installment_floating

        # Hitung rasio cicilan terhadap pendapatan (dalam persen)
        income_to_installment_ratio = (installment_for_ratio / monthly_income) * Decimal('100')

        # Tentukan status berdasarkan rasio
        # Rule of thumb: cicilan KPR sebaiknya tidak lebih dari 30% pendapatan
        SAFE_RATIO_THRESHOLD = Decimal('30')  # 30%

        if income_to_installment_ratio <= SAFE_RATIO_THRESHOLD:
            calc_status = "mampu"
            is_suitable = True
            recommendation = (
                f"Selamat! KPR ini tergolong affordable untuk Anda. "
                f"Dengan harga properti Rp {property_price:,.0f} dan DP {dp_percentage}% "
                f"(Rp {dp_amount:,.0f}), jumlah pinjaman Anda adalah Rp {loan_amount:,.0f}. "
                f"Cicilan bulanan periode fixed ({fixed_period_months} bulan pertama) "
                f"sekitar Rp {monthly_installment_fixed:,.0f}, "
                f"lalu setelah itu dengan bunga floating menjadi Rp {monthly_installment_floating:,.0f}. "
                f"Rasio cicilan terhadap pendapatan Anda adalah {income_to_installment_ratio:.2f}%, "
                f"yang masih di bawah batas aman 30%. "
                f"Pastikan Anda memiliki dana darurat minimal 6 bulan pengeluaran sebelum mengambil KPR."
            )
        else:
            calc_status = "tidak mampu"
            is_suitable = False
            excess_ratio = income_to_installment_ratio - SAFE_RATIO_THRESHOLD
            
            # Hitung DP yang dibutuhkan agar ratio jadi safe
            max_safe_installment = monthly_income * (SAFE_RATIO_THRESHOLD / Decimal('100'))
            
            if monthly_floating_rate > 0:
                # Reverse calculate loan amount from safe installment
                safe_loan_amount = max_safe_installment * (
                    (growth_factor_floating - Decimal('1')) / (monthly_floating_rate * growth_factor_floating)
                )
            else:
                safe_loan_amount = max_safe_installment * loan_term_months
            
            recommended_dp = property_price - safe_loan_amount
            recommended_dp_pct = (recommended_dp / property_price) * Decimal('100')
            
            recommendation = (
                f"Perhatian! KPR ini mungkin terlalu berat untuk keuangan Anda. "
                f"Dengan pendapatan Rp {monthly_income:,.0f}/bulan dan cicilan "
                f"Rp {monthly_installment_floating:,.0f}/bulan (floating rate), "
                f"rasio cicilan terhadap pendapatan Anda adalah {income_to_installment_ratio:.2f}%, "
                f"melebihi batas aman 30% sebesar {excess_ratio:.2f}%. "
                f"Untuk membuat KPR ini lebih affordable, Anda bisa: "
                f"1) Tingkatkan DP menjadi sekitar {recommended_dp_pct:.1f}% "
                f"(Rp {recommended_dp:,.0f}), atau "
                f"2) Perpanjang tenor KPR untuk mengurangi cicilan bulanan, atau "
                f"3) Cari properti dengan harga lebih rendah (sekitar Rp {safe_loan_amount + dp_amount:,.0f}), atau "
                f"4) Tingkatkan pendapatan bulanan Anda terlebih dahulu. "
                f"Bank mungkin menolak pengajuan KPR jika rasio melebihi 30-40%."
            )

        # Simpan dengan hasil perhitungan
        serializer.save(
            user=self.request.user,
            dp_amount=dp_amount,
            loan_amount=loan_amount,
            monthly_installment_fixed=monthly_installment_fixed,
            monthly_installment_floating=monthly_installment_floating,
            income_to_installment_ratio=income_to_installment_ratio,
            status=calc_status,
            is_suitable=is_suitable,
            recommendation=recommendation
        )
