from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
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
    gap_now = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )  # selisih dana sekarang
    status = models.CharField(
        max_length=30,
        blank=True, null=True
    )  # contoh: 'Tercapai', 'Kurang Dana'
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'calc_marriage'
        verbose_name = "Marriage Calculation"
        
    def __str__(self):
        return f"Marriage Calculation #{self.pk} for {self.user}"
>>>>>>> 44da526b83f40d4dc6b1ef904768a5b18d335807
