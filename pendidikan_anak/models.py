from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from django.conf import settings   # <-- WAJIB

class ChildEducationCalculation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,        
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='child_education_calculations'
    )
    
    # --- Data Input ---
    child_age_years = models.DecimalField(max_digits=5, decimal_places=2)
    college_years_ahead = models.DecimalField(max_digits=5, decimal_places=2)
    current_tuition = models.DecimalField(max_digits=18, decimal_places=2)
    inflation_pct = models.DecimalField(max_digits=6, decimal_places=3)
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2)
    expected_return_pct = models.DecimalField(max_digits=6, decimal_places=3)
    
    # --- Data Output (nullable) ---
    total_future_need = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )
    monthly_needed = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calc_child_education'
        verbose_name = "Child Education Calculation"

    def __str__(self):
        return f"Child Education Calculation #{self.pk} for {self.user}"
>>>>>>> 44da526b83f40d4dc6b1ef904768a5b18d335807
