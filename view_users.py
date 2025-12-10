#!/usr/bin/env python
"""
View All Registered Users
==========================
Script untuk melihat semua user yang sudah registrasi.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalkulatorInvestasi.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def view_all_users():
    """Display all registered users"""
    
    print("=" * 80)
    print("  REGISTERED USERS")
    print("=" * 80)
    
    users = User.objects.all().order_by('-date_joined')
    
    if not users:
        print("\n⚠️  No users found in database")
        print("   Register a user via: POST /api/auth/register/\n")
        return
    
    print(f"\n📊 Total Users: {users.count()}")
    
    # Count by role
    user_count = users.filter(role='USER').count()
    admin_count = users.filter(role='ADMIN').count()
    print(f"   - Regular Users: {user_count}")
    print(f"   - Admins: {admin_count}")
    
    print("\n" + "-" * 80)
    print(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Full Name':<20} {'Role':<8} {'Active':<8}")
    print("-" * 80)
    
    for user in users:
        print(f"{user.id:<5} {user.username:<15} {user.email:<25} "
              f"{(user.full_name or '-'):<20} {user.role:<8} "
              f"{'Yes' if user.is_active else 'No':<8}")
    
    print("-" * 80)
    
    # Detailed view option
    print("\n📋 Detailed View:")
    print("-" * 80)
    
    for user in users:
        print(f"\n👤 User #{user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Full Name: {user.full_name or '-'}")
        print(f"   Phone: {user.phone_number or '-'}")
        print(f"   Role: {user.get_role_display()}")
        print(f"   Active: {user.is_active}")
        print(f"   Registered: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if user.last_login:
            print(f"   Last Login: {user.last_login.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"   Last Login: Never")
        
        # Count calculations
        total_calcs = 0
        if hasattr(user, 'emergency_fund_calculations'):
            total_calcs += user.emergency_fund_calculations.count()
        if hasattr(user, 'pension_records'):
            total_calcs += user.pension_records.count()
        if hasattr(user, 'goldcalculation_set'):
            total_calcs += user.goldcalculation_set.count()
        
        print(f"   Total Calculations: {total_calcs}")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    try:
        view_all_users()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
