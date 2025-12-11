from django.db import models

# Create your models here.
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
    college_entry_age = models.DecimalField(max_digits=5, decimal_places=2)  # Usia masuk kuliah
    current_tuition_per_year = models.DecimalField(max_digits=18, decimal_places=2)
    college_duration_years = models.IntegerField(default=4)  # Lama kuliah
    education_inflation_pct = models.DecimalField(max_digits=6, decimal_places=3)
    current_saving = models.DecimalField(max_digits=18, decimal_places=2)
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2)
    expected_return_pct = models.DecimalField(max_digits=6, decimal_places=3)
    
    # --- Data Output (nullable) ---
    years_until_college = models.IntegerField(blank=True, null=True)
    future_tuition_per_year = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )
    total_education_need = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )
    future_value = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )
    gap_amount = models.DecimalField(
        max_digits=18, decimal_places=2,
        blank=True, null=True
    )
    status = models.CharField(
        max_length=30,
        blank=True, null=True
    )
    
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
        db_table = 'calc_child_education'
        verbose_name = "Child Education Calculation"

    def __str__(self):
        return f"Child Education Calculation #{self.pk} for {self.user}"
