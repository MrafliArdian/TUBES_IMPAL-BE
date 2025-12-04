<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
# dana_darurat/views.py
from decimal import Decimal
from rest_framework import viewsets, permissions

from .models import EmergencyFundCalculation
from .serializers import EmergencyFundSerializer


def hitung_dana_darurat(
    monthly_expense: Decimal,
    months_to_save: int,
    current_emergency_fund: Decimal,
    monthly_invest: Decimal,
    expected_return_pct: Decimal,
):
    n = int(months_to_save)

    # kebutuhan dana darurat
    needed_fund = monthly_expense * n

    # konversi return ke bulanan
    r_year = Decimal(expected_return_pct) / Decimal('100')       # contoh: 10 -> 0.10
    r_month = r_year / Decimal('12')                             # per bulan

    if r_month > 0:
        # Future value dari dana darurat yang sudah ada
        fv_current = current_emergency_fund * (1 + r_month) ** n

        # Future value dari setoran bulanan (anuitas)
        fv_invest = monthly_invest * (((1 + r_month) ** n - 1) / r_month)
    else:
        # tanpa bunga
        fv_current = current_emergency_fund
        fv_invest = monthly_invest * n

    future_value = fv_current + fv_invest
    gap_amount = future_value - needed_fund

    status = 'cukup' if future_value >= needed_fund else 'tidak cukup'

    return needed_fund, future_value, gap_amount, status


class EmergencyFundViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencyFundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # tiap user hanya bisa lihat riwayat perhitungan miliknya sendiri
        return EmergencyFundCalculation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = serializer.validated_data

        needed_fund, future_value, gap_amount, status = hitung_dana_darurat(
            monthly_expense=data['monthly_expense'],
            months_to_save=data['months_to_save'],
            current_emergency_fund=data['current_emergency_fund'],
            monthly_invest=data['monthly_invest'],
            expected_return_pct=data['expected_return_pct'],
        )

        serializer.save(
            user=self.request.user,
            needed_fund=needed_fund,
            future_value=future_value,
            gap_amount=gap_amount,
            status=status,
        )

    def perform_update(self, serializer):
        # kalau user edit input, hitung ulang output
        data = serializer.validated_data

        needed_fund, future_value, gap_amount, status = hitung_dana_darurat(
            monthly_expense=data['monthly_expense'],
            months_to_save=data['months_to_save'],
            current_emergency_fund=data['current_emergency_fund'],
            monthly_invest=data['monthly_invest'],
            expected_return_pct=data['expected_return_pct'],
        )

        serializer.save(
            needed_fund=needed_fund,
            future_value=future_value,
            gap_amount=gap_amount,
            status=status,
        )
>>>>>>> 44da526b83f40d4dc6b1ef904768a5b18d335807
