from django.db import models

# Create your models here.
class MarriageCalculation(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    
    # --- Data Input Pernikahan ---
    target_cost = models.DecimalField(max_digits=18, decimal_places=2) 
    current_saving = models.DecimalField(max_digits=18, decimal_places=2) 
    months_to_event = models.IntegerField()
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2) 
    expected_return_pct = models.DecimalField(max_digits=6, decimal_places=3)
    
    # --- Data Output (Bisa NULL jika perhitungan belum selesai) ---
    gap_now = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True) # Kekurangan/kelebihan dana saat ini
    status = models.CharField(max_length=30, blank=True, null=True) # Misalnya: 'Tercapai', 'Kurang Dana'
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'calc_marriage'
        verbose_name = "Marriage Calculation"
        
    def __str__(self):
        return f"Pernikahan: {self.user.full_name} ({self.created_at.strftime('%Y-%m-%d')})"
  