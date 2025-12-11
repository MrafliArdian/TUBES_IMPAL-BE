from django.db import models
from django.conf import settings

class SimulasiKPR(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mortgage_simulations'
    )
    
    # --- Data Input ---
    property_price = models.DecimalField(max_digits=18, decimal_places=2)
    monthly_income = models.DecimalField(max_digits=18, decimal_places=2)
    dp_percentage = models.DecimalField(max_digits=6, decimal_places=3)  # %
    loan_term_months = models.IntegerField()  # Tenor dalam bulan
    fixed_interest_rate = models.DecimalField(max_digits=6, decimal_places=3)  # % per tahun
    fixed_period_months = models.IntegerField()  # Berapa bulan bunga fix
    floating_interest_rate = models.DecimalField(max_digits=6, decimal_places=3)  # % per tahun
    
    # --- Data Output ---
    dp_amount = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )
    loan_amount = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )
    monthly_installment_fixed = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )
    monthly_installment_floating = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )
    income_to_installment_ratio = models.DecimalField(
        max_digits=6, decimal_places=3,
        blank=True, null=True
    )  # Ratio cicilan/pendapatan dalam persen
    status = models.CharField(
        max_length=30,
        blank=True, null=True
    )  # "mampu" / "tidak mampu"
    
    # --- Recommendations ---
    is_suitable = models.BooleanField(
        default=False,
        help_text='True jika KPR affordable (ratio < 30%)'
    )
    recommendation = models.TextField(
        blank=True,
        null=True,
        help_text='Saran untuk user berdasarkan hasil simulasi'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'calc_mortgage'
        verbose_name = "Simulasi KPR"
    
    def __str__(self):
        return f"KPR Simulation #{self.pk} for {self.user}"