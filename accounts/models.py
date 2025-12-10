from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom User model dengan role-based access control.
    - USER: Regular user yang bisa menggunakan kalkulator dan menyimpan history
    - ADMIN: Admin yang bisa melihat semua user dan data mereka
    """
    
    ROLE_CHOICES = [
        ('USER', 'Regular User'),
        ('ADMIN', 'Administrator'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='USER',
        help_text='User role untuk access control'
    )
    
    full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Nama lengkap user'
    )
    
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Nomor telepon user'
    )
    
    class Meta:
        db_table = 'accounts_customuser'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'ADMIN'
    
    @property
    def is_regular_user(self):
        """Check if user is regular user"""
        return self.role == 'USER'
