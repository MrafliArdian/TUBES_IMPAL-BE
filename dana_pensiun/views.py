<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
# dana_pensiun/views.py
from decimal import Decimal
from rest_framework import viewsets, permissions

from .models import PensionCalculation
from .serializers import PensionSerializer


def hitung_dana_pensiun(
    current_age: int,
    retire_age: int,
    monthly_expense_now: Decimal,
    inflation_pct: Decimal,
    expected_return_pct: Decimal,
    pension_years: int,
    monthly_invest: Decimal,
):
    """
    Implementasi Psucode doang
    Perhitungan sederhana Dana Pensiun sesuai field di tabelmu.

    1. Hitung pengeluaran bulanan pada saat pensiun:
       years = retire_age - current_age
       monthly_expense_at_retire = monthly_expense_now * (1 + inflasi)^years

    2. Total kebutuhan dana pensiun:
       total_need = monthly_expense_at_retire * 12 * pension_years

    3. Estimasi portofolio:
       n = years * 12
       r_year = expected_return_pct / 100
       r_month = r_year / 12

       estimated_portfolio = FV dari investasi bulanan:
         FV = monthly_invest * ((1 + r_month)^n - 1) / r_month
       kalau r_month = 0 → FV = monthly_invest * n

    4. Status:
       "cukup" kalau estimated_portfolio ≥ total_need
       else "tidak cukup"
    """

    years_until_retire = max(retire_age - current_age, 0)
    n_months = years_until_retire * 12

    # inflasi & return dalam bentuk desimal
    infl = Decimal(inflation_pct) / Decimal('100')
    r_year = Decimal(expected_return_pct) / Decimal('100')

    # pengeluaran saat pensiun (sudah kena inflasi tahunan)
    if years_until_retire > 0 and infl != 0:
        monthly_at_retire = monthly_expense_now * (1 + infl) ** years_until_retire
    else:
        monthly_at_retire = monthly_expense_now

    # total kebutuhan selama masa pensiun
    total_need = monthly_at_retire * Decimal('12') * Decimal(pension_years)

    # hitung portofolio dari investasi bulanan
    r_month = r_year / Decimal('12') if r_year != 0 else Decimal('0')

    if n_months > 0 and r_month != 0:
        estimated_portfolio = (
            monthly_invest
            * ((1 + r_month) ** n_months - 1)
            / r_month
        )
    else:
        # tidak ada bunga atau tidak ada waktu investasi
        estimated_portfolio = monthly_invest * n_months

    status = 'cukup' if estimated_portfolio >= total_need else 'tidak cukup'

    return total_need, estimated_portfolio, status


class PensionViewSet(viewsets.ModelViewSet):
    """
    Endpoint CRUD Dana Pensiun:
    - GET /api/dana-pensiun/          -> list data user
    - POST /api/dana-pensiun/         -> buat + hitung
    - GET /api/dana-pensiun/{id}/     -> detail
    - PUT/PATCH /api/dana-pensiun/{id}/ -> update + hitung ulang
    - DELETE /api/dana-pensiun/{id}/  -> hapus
    """

    serializer_class = PensionSerializer
    permission_classes = [permissions.IsAuthenticated]
    # kalau mau tes tanpa login:
    # permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return PensionCalculation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = serializer.validated_data

        total_need, estimated_portfolio, status = hitung_dana_pensiun(
            current_age=data['current_age'],
            retire_age=data['retire_age'],
            monthly_expense_now=data['monthly_expense_now'],
            inflation_pct=data['inflation_pct'],
            expected_return_pct=data['expected_return_pct'],
            pension_years=data['pension_years'],
            monthly_invest=data['monthly_invest'],
        )

        serializer.save(
            user=self.request.user,
            total_need_at_retire=total_need,
            estimated_portfolio=estimated_portfolio,
            status=status,
        )

    def perform_update(self, serializer):
        data = serializer.validated_data

        total_need, estimated_portfolio, status = hitung_dana_pensiun(
            current_age=data['current_age'],
            retire_age=data['retire_age'],
            monthly_expense_now=data['monthly_expense_now'],
            inflation_pct=data['inflation_pct'],
            expected_return_pct=data['expected_return_pct'],
            pension_years=data['pension_years'],
            monthly_invest=data['monthly_invest'],
        )

        serializer.save(
            total_need_at_retire=total_need,
            estimated_portfolio=estimated_portfolio,
            status=status,
        )
>>>>>>> 44da526b83f40d4dc6b1ef904768a5b18d335807
