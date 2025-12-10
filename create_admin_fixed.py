#!/usr/bin/env python
"""
Create Admin User - FIXED VERSION
==================================
Script dengan transaction handling dan verification yang proper.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalkulatorInvestasi.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

def create_admin_user():
    """Create admin user dengan proper transaction handling"""
    
    print("=" * 60)
    print("  CREATE ADMIN USER - FIXED")
    print("=" * 60)
    
    username = "admin"
    email = "admin@gmail.com"
    password = "AdminPass123!"
    full_name = "Administrator"
    
    print(f"\n[*] Creating admin user...")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   Full Name: {full_name}")
    
    try:
        # Use transaction to ensure data is saved
        with transaction.atomic():
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                print(f"\n[WARN] User '{username}' already exists!")
                
                user = User.objects.get(username=username)
                print(f"\n[*] Current user info:")
                print(f"   ID: {user.id}")
                print(f"   Role: {user.role}")
                print(f"   Active: {user.is_active}")
                
                update = input("\n[?] Update to ADMIN and reset password? (y/n): ").strip().lower()
                
                if update == 'y':
                    user.role = 'ADMIN'
                    user.set_password(password)
                    user.email = email
                    user.full_name = full_name
                    user.is_active = True
                    user.save()
                    
                    print(f"\n[OK] User updated successfully!")
                else:
                    print(f"\n[INFO] No changes made.")
                    return user
            else:
                # Create new admin user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    full_name=full_name,
                    role='ADMIN',
                    is_active=True
                )
                
                print(f"\n[OK] Admin user created!")
            
            # Force save to ensure it's in database
            user.save()
            
            # Verify it was saved
            print(f"\n[*] Verifying user in database...")
            verify_user = User.objects.get(username=username)
            
            print(f"[OK] User verified in database!")
            print(f"   ID: {verify_user.id}")
            print(f"   Username: {verify_user.username}")
            print(f"   Email: {verify_user.email}")
            print(f"   Role: {verify_user.role} ({verify_user.get_role_display()})")
            print(f"   Active: {verify_user.is_active}")
            
            # Test password
            if verify_user.check_password(password):
                print(f"   Password: [OK]")
            else:
                print(f"   Password: [ERROR] Password verification failed!")
                raise Exception("Password verification failed")
            
            print(f"\n" + "=" * 60)
            print("[SUCCESS] ADMIN USER READY")
            print("=" * 60)
            
            print(f"\n[*] Login via Postman:")
            print(f"   POST http://localhost:8000/api/auth/login/")
            print(f"   {{")
            print(f'     "username": "{username}",')
            print(f'     "password": "{password}"')
            print(f"   }}")
            
            print(f"\n[*] Quick verification:")
            print(f"   python verify_admin.py")
            print()
            
            return user
            
    except Exception as e:
        print(f"\n[ERROR] Failed to create admin user!")
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    try:
        user = create_admin_user()
        if user:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[WARN] Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
