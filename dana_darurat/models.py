# dana_darurat/models.py
from django.db import models
from django.conf import settings


class EmergencyFundCalculation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='emergency_fund_calculations'
    )

    # --- INPUT dari form UI ---
    # Pengeluaran wajib bulanan
    monthly_expense = models.DecimalField(max_digits=18, decimal_places=2)

    # Berapa bulan untuk mengumpulkan dana darurat
    months_to_save = models.IntegerField()

    # Dana darurat yang sudah dimiliki saat ini
    current_emergency_fund = models.DecimalField(max_digits=18, decimal_places=2)

    # Target investasi bulanan
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2)

    # Target return investasi per tahun (dalam persen, misal 10 untuk 10%)
    expected_return_pct = models.DecimalField(max_digits=5, decimal_places=2)

    # --- OUTPUT hasil perhitungan ---
    # Dana darurat yang dibutuhkan = monthly_expense * months_to_save
    needed_fund = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )

    # Estimasi nilai investasi terkumpul
    future_value = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )

    # Selisih future_value - needed_fund (bisa minus)
    gap_amount = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )

    # "cukup" atau "tidak cukup"
    status = models.CharField(
        max_length=20,
        blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calc_emergency_fund'
        ordering = ['-created_at']

    def __str__(self):
        return f"Dana Darurat {self.user} - {self.created_at.date()}"
