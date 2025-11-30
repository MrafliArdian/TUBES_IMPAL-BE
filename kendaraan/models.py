from django.db import models
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
    down_payment = models.DecimalField(max_digits=18, decimal_places=2)
    current_saving = models.DecimalField(max_digits=18, decimal_places=2)
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2)
    expected_return_pct = models.DecimalField(max_digits=6, decimal_places=3)

    # --- Data Output ---
    needed_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    status = models.CharField(
        max_length=30, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calc_vehicle'
        verbose_name = "Vehicle Calculation"

    def __str__(self):
        # jangan assume ada full_name, pakai repr user saja
        return f"Vehicle calc #{self.pk} for {self.user}"
