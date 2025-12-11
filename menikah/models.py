from django.db import models
# Create your models here.

from django.conf import settings  # <-- penting

class MarriageCalculation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,        # <-- bukan 'User'
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='marriage_calculations'
    )
    
    # --- Data Input Pernikahan ---
    target_cost = models.DecimalField(max_digits=18, decimal_places=2)
    current_saving = models.DecimalField(max_digits=18, decimal_places=2)
    months_to_event = models.IntegerField()
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2)
    expected_return_pct = models.DecimalField(max_digits=6, decimal_places=3)
    
    # --- Data Output (Bisa NULL jika perhitungan belum selesai) ---
    future_value = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )  # Total dana di masa depan
    gap_amount = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )  # selisih (target_cost - future_value)
    status = models.CharField(
        max_length=30,
        blank=True, null=True
    )  # contoh: 'cukup', 'tidak cukup'
    
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
        db_table = 'calc_marriage'
        verbose_name = "Marriage Calculation"
        
    def __str__(self):
        return f"Marriage Calculation #{self.pk} for {self.user}"
