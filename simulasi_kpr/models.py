from django.db import models

# Create your models here.
from django.conf import settings

class SimulasiKPR(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    harga_properti = models.FloatField()
    penghasilan = models.FloatField()
    dp_percent = models.FloatField()
    tenor_bulan = models.IntegerField()
    bunga_fix = models.FloatField()
    periode_fix = models.IntegerField()
    bunga_floating = models.FloatField()
    pokok_pinjaman = models.FloatField()
    total_bunga_fix = models.FloatField()
    total_bunga_floating = models.FloatField()
    sisa_pokok_setelah_fix = models.FloatField()
    keterangan = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)