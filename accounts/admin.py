# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface untuk CustomUser model"""
    
    # Fields yang ditampilkan di list view
    list_display = ('username', 'email', 'full_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'full_name', 'phone_number')
    
    # Fieldsets untuk form view
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'full_name', 'phone_number')
        }),
    )
    
    # Fields yang bisa diedit saat add user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'full_name', 'phone_number', 'email')
        }),
    )
    
    # Enable actions untuk mengubah role
    actions = ['make_admin', 'make_user']
    
    def make_admin(self, request, queryset):
        """Action untuk promote user menjadi admin"""
        updated = queryset.update(role='ADMIN')
        self.message_user(request, f'{updated} user berhasil dijadikan admin.')
    make_admin.short_description = "Promote selected users to ADMIN"
    
    def make_user(self, request, queryset):
        """Action untuk demote admin menjadi user"""
        updated = queryset.update(role='USER')
        self.message_user(request, f'{updated} admin berhasil dijadikan user biasa.')
    make_user.short_description = "Demote selected users to USER"
