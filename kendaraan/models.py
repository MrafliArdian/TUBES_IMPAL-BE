from django.db import models

# Create your models here.
<<<<<<< HEAD
=======
class VehicleCalculation(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    
    # --- Data Input Kendaraan ---
    vehicle_price = models.DecimalField(max_digits=18, decimal_places=2) 
    down_payment = models.DecimalField(max_digits=18, decimal_places=2) 
    current_saving = models.DecimalField(max_digits=18, decimal_places=2) 
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2) 
    expected_return_pct = models.DecimalField(max_digits=6, decimal_places=3)
    
    # --- Data Output (Bisa NULL jika perhitungan belum selesai) ---
    needed_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True) # Kekurangan/kelebihan dana saat ini
    status = models.CharField(max_length=30, blank=True, null=True) # Misalnya: 'Tercapai', 'Perlu Investasi Tambahan'
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'calc_vehicle'
        verbose_name = "Vehicle Calculation"
        
    def __str__(self):
        return f"Kendaraan: {self.user.full_name} ({self.created_at.strftime('%Y-%m-%d')})"
>>>>>>> Dev_Nada
