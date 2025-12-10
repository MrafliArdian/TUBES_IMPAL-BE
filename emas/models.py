from django.db import models
# Create your models here.

from django.conf import settings

class GoldCalculation(models.Model):

    MODE_CHOICES = [
        ('emas_to_rupiah', 'Emas → Rupiah'),
        ('rupiah_to_emas', 'Rupiah → Emas'),
    ]

    PRICE_CHOICES = [
        ('BUY', 'Harga Beli'),
        ('SELL', 'Harga Jual'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id'
    )

    mode = models.CharField(max_length=20, choices=MODE_CHOICES)

    price_choice = models.CharField(max_length=4, choices=PRICE_CHOICES)

    grams_input = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    rupiah_input = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    price_per_gram = models.DecimalField(max_digits=18, decimal_places=2)

    result_rupiah = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    result_grams = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True)
    
    # Catatan tambahan untuk user
    notes = models.TextField(
        blank=True, null=True,
        help_text='Catatan atau insight tentang investasi emas'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calc_gold'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.mode} - {self.user_id}"
