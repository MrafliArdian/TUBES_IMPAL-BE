from django.db import models
from django.db.models import JSONField

class User(models.Model):
        full_name = models.CharField(max_length=100)
        email = models.EmailField(max_length=120, unique=True)
        phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
        password_hash = models.CharField(max_length=128)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
                db_table = 'users'

        def __str__(self):
                return self.email

class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'roles'
        
    def __str__(self):
        return self.role_name
    
class UserRole(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    
    role = models.ForeignKey(
        'Role', 
        on_delete=models.CASCADE, 
        db_column='role_id'
    )

    class Meta:
        db_table = 'user_roles' 
        
        unique_together = (('user', 'role'),) 
        
        verbose_name = "User Role Assignment"

    def __str__(self):
        return f"{self.user.email} - {self.role.role_name}"
    
CALCULATOR_CHOICES = (
    ('child_education', 'Pendidikan Anak'),
    ('kpr', 'KPR'),
    ('emergency_fund', 'Dana Darurat'),
    ('pension', 'Pensiun'),
    ('marriage', 'Pernikahan'),
    ('vehicle', 'Kendaraan'),
    ('gold', 'Emas'),
)

class Calculation(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    
    calculator_type = models.CharField(
        max_length=20, 
        choices=CALCULATOR_CHOICES,
        default='child_education'
    )

    title = models.CharField(max_length=120, blank=True, null=True)

    input_data = JSONField() 
    
    result_data = JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'calculations'
        verbose_name_plural = "Calculations"

        indexes = [
            models.Index(fields=['user', 'created_at'], name='idx_calculations_user'),
            
            models.Index(fields=['calculator_type', 'created_at'], name='idx_calculations_type'),
        ]
        
    def __str__(self):
        return f"{self.user.full_name} - {self.title or self.calculator_type}"
    
class ChildEducationCalculation(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    
    # --- Data Input ---
    child_age_years = models.DecimalField(max_digits=5, decimal_places=2) 
    college_years_ahead = models.DecimalField(max_digits=5, decimal_places=2) 
    current_tuition = models.DecimalField(max_digits=18, decimal_places=2) 
    inflation_pct = models.DecimalField(max_digits=6, decimal_places=3) 
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2) 
    expected_return_pct = models.DecimalField(max_digits=6, decimal_places=3) 
    
    # --- Data Output (Bisa NULL jika perhitungan belum selesai) ---
    total_future_need = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    monthly_needed = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'calc_child_education'
        verbose_name = "Child Education Calculation"
        
    def __str__(self):
        return f"Edukasi Anak: {self.user.full_name} ({self.created_at.strftime('%Y-%m-%d')})"
    
class KprCalculation(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    
    # --- Data Input KPR ---
    house_price = models.DecimalField(max_digits=18, decimal_places=2) 
    down_payment = models.DecimalField(max_digits=18, decimal_places=2) 
    tenor_months = models.IntegerField()
    fix_rate_pct = models.DecimalField(max_digits=6, decimal_places=3)
    fix_period_months = models.IntegerField()
    floating_rate_pct = models.DecimalField(max_digits=6, decimal_places=3)
    
    # --- Data Output (Bisa NULL jika perhitungan belum selesai) ---
    monthly_installment = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_interest_fix = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_interest_floating = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'calc_kpr'
        verbose_name = "KPR Calculation"
        
    def __str__(self):
        return f"KPR: {self.user.full_name} ({self.created_at.strftime('%Y-%m-%d')})"
    
class EmergencyFundCalculation(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    
    # --- Data Input Dana Darurat ---
    monthly_expense = models.DecimalField(max_digits=18, decimal_places=2) 
    target_months = models.IntegerField()
    current_fund = models.DecimalField(max_digits=18, decimal_places=2) 
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2) 
    expected_return_pct = models.DecimalField(max_digits=6, decimal_places=3)
    
    # --- Data Output (Bisa NULL jika perhitungan belum selesai) ---
    target_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    months_to_reach = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'calc_emergency_fund'
        verbose_name = "Emergency Fund Calculation"
        
    def __str__(self):
        return f"Dana Darurat: {self.user.full_name} ({self.created_at.strftime('%Y-%m-%d')})"
    
class PensionCalculation(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    
    # --- Data Input Pensiun ---
    current_age = models.IntegerField()
    retire_age = models.IntegerField()
    monthly_expense_now = models.DecimalField(max_digits=18, decimal_places=2) 
    inflation_pct = models.DecimalField(max_digits=6, decimal_places=3)
    expected_return_pct = models.DecimalField(max_digits=6, decimal_places=3)
    pension_years = models.IntegerField()
    monthly_invest = models.DecimalField(max_digits=18, decimal_places=2) 
    
    # --- Data Output (Bisa NULL jika perhitungan belum selesai) ---
    total_need_at_retire = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    estimated_portfolio = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True) # Misalnya: 'Aman', 'Kurang'
    
    created_at = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        db_table = 'calc_pensiun'
        verbose_name = "Pension Calculation"
        
    def __str__(self):
        return f"Pensiun: {self.user.full_name} ({self.created_at.strftime('%Y-%m-%d')})"
    
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
    
GOLD_MODE_CHOICES = (
    ('emas_to_rupiah', 'Emas ke Rupiah'),
    ('rupiah_to_emas', 'Rupiah ke Emas'),
)

GOLD_PRICE_CHOICES = (
    ('BUY', 'Beli'),
    ('SELL', 'Jual'),
)

class GoldCalculation(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    
    # --- Data Input Emas ---
    mode = models.CharField(max_length=20, choices=GOLD_MODE_CHOICES) 
    price_choice = models.CharField(max_length=5, choices=GOLD_PRICE_CHOICES)
    
    # Input data (boleh kosong tergantung mode)
    grams_input = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    rupiah_input = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    price_per_gram = models.DecimalField(max_digits=18, decimal_places=2) 
    
    # --- Data Output (Bisa NULL jika perhitungan belum selesai) ---
    result_rupiah = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    result_grams = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'calc_gold'
        verbose_name = "Gold Calculation"

        indexes = [
            models.Index(fields=['user', 'created_at'], name='idx_calc_gold_user'),
        ]
        
    def __str__(self):
        return f"Emas: {self.user.full_name} ({self.created_at.strftime('%Y-%m-%d')})"
    
class Article(models.Model):
    author = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL,
        db_column='author_id',
        null=True, # <--- Memungkinkan NULL di DB
        blank=True # Memungkinkan field kosong di form Django
    )
    
    title = models.CharField(max_length=200) 
    
    content = models.TextField() 
    
    # image_url (TEXT, boleh NULL)
    image_url = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'articles'
        verbose_name_plural = "Articles"
        
    def __str__(self):
        return self.title