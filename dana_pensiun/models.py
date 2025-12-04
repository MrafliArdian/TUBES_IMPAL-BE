from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from django.conf import settings


class PensionCalculation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='pension_records'
    )

    current_age = models.IntegerField()
    retire_age = models.IntegerField()

    monthly_expense_now = models.DecimalField(max_digits=18, decimal_places=2)
    inflation_pct = models.DecimalField(max_digits=5, decimal_places=2)
    expected_return_pct = models.DecimalField(max_digits=5, decimal_places=2)

    pension_years = models.IntegerField()
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2)

    total_need_at_retire = models.DecimalField(
        max_digits=18, decimal_places=2,
        null=True, blank=True
    )
    estimated_portfolio = models.DecimalField(
        max_digits=18, decimal_places=2,
        null=True, blank=True
    )
    status = models.CharField(
        max_length=20,
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calc_pensiun'
        ordering = ['-created_at']

    def __str__(self):
        return f"Pension {self.user} - {self.created_at.date()}"
>>>>>>> 44da526b83f40d4dc6b1ef904768a5b18d335807
