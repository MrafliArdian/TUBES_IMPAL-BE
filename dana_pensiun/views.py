from django.shortcuts import render

# Create your views here.
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
        
        # Generate recommendation
        is_suitable = (status == 'cukup')
        years_until_retire = max(data['retire_age'] - data['current_age'], 0)
        
        if is_suitable:
            surplus = estimated_portfolio - total_need
            recommendation = (
                f"Selamat! Persiapan pensiun Anda sudah mencukupi. "
                f"Dengan investasi bulanan Rp {data['monthly_invest']:,.0f} selama {years_until_retire} tahun, "
                f"estimasi portofolio Anda saat pensiun adalah Rp {estimated_portfolio:,.0f}, "
                f"melebihi kebutuhan pensiun Rp {total_need:,.0f} untuk {data['pension_years']} tahun. "
                f"Kelebihan dana sebesar Rp {surplus:,.0f} dapat menjadi buffer atau warisan."
            )
        else:
            shortfall = total_need - estimated_portfolio
            months_until_retire = years_until_retire * 12
            additional_monthly = shortfall / months_until_retire if months_until_retire > 0 else shortfall
            recommendation = (
                f"Dana pensiun Anda masih kurang. Target kebutuhan untuk {data['pension_years']} tahun pensiun "
                f"adalah Rp {total_need:,.0f}, namun dengan investasi saat ini hanya akan terkumpul Rp {estimated_portfolio:,.0f}. "
                f"Kekurangan: Rp {shortfall:,.0f}. "
                f"Pertimbangkan untuk menambah investasi bulanan sekitar Rp {additional_monthly:,.0f} "
                f"atau memperpanjang masa kerja sebelum pensiun."
            )

        serializer.save(
            user=self.request.user,
            total_need_at_retire=total_need,
            estimated_portfolio=estimated_portfolio,
            status=status,
            recommendation=recommendation,
            is_suitable=is_suitable,
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
