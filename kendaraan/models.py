from django.db import models
# Create your models here.
from django.conf import settings  # ⬅️ penting

class VehicleCalculation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,        # ⬅️ bukan 'User' string lagi
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='vehicle_calculations'  # nama bebas, hanya untuk akses balik
    )
    
    # --- Data Input Kendaraan ---
    vehicle_price = models.DecimalField(max_digits=18, decimal_places=2)
    down_payment = models.DecimalField(max_digits=18, decimal_places=2)  # DP amount in rupiah
    current_saving = models.DecimalField(max_digits=18, decimal_places=2)
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2)
    expected_return_pct = models.DecimalField(max_digits=6, decimal_places=3)  # per tahun
    investment_period_months = models.IntegerField()  # berapa bulan mau invest

    # --- Data Output ---
    needed_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    future_value = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )  # Total dana di masa depan
    gap_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )  # Selisih (future_value - needed_amount)
    status = models.CharField(
        max_length=30, blank=True, null=True
    )  # "cukup" / "tidak cukup"
    
    # --- Recommendations ---
    is_suitable = models.BooleanField(
        default=False,
        help_text='True jika strategi investasi cocok/mencukupi'
    )
    recommendation = models.TextField(
        blank=True,
        null=True,
        help_text='Saran untuk user berdasarkan hasil kalkulasi'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calc_vehicle'
        verbose_name = "Vehicle Calculation"

    def __str__(self):
        # jangan assume ada full_name, pakai repr user saja
        return f"Vehicle calc #{self.pk} for {self.user}"
