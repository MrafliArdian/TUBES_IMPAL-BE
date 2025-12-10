#!/usr/bin/env python
"""
Verify Admin User & Test Login
================================
Script untuk verify admin user exists dan test authentication.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalkulatorInvestasi.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

def verify_admin_user():
    """Verify admin user dan test authentication"""
    
    print("=" * 60)
    print("  ADMIN USER VERIFICATION")
    print("=" * 60)
    
    username = "admin"
    password = "AdminPass123!"
    
    # Check if user exists
    print(f"\n[*] Checking user '{username}'...")
    
    try:
        user = User.objects.get(username=username)
        print(f"[OK] User found!")
        print(f"   ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Full Name: {user.full_name}")
        print(f"   Role: {user.role} ({user.get_role_display()})")
        print(f"   Is Active: {user.is_active}")
        print(f"   Is Staff: {user.is_staff}")
        print(f"   Is Superuser: {user.is_superuser}")
        
        # Test password
        print(f"\n[*] Testing password...")
        if user.check_password(password):
            print(f"[OK] Password is correct!")
        else:
            print(f"[ERROR] Password is INCORRECT!")
            print(f"   The password stored in database doesn't match '{password}'")
            print(f"\n[FIX] Reset password:")
            print(f"   user = User.objects.get(username='{username}')")
            print(f"   user.set_password('{password}')")
            print(f"   user.save()")
            return False
        
        # Test Django authenticate
        print(f"\n[*] Testing Django authenticate()...")
        auth_user = authenticate(username=username, password=password)
        
        if auth_user:
            print(f"[OK] Django authentication successful!")
            print(f"   User: {auth_user.username}")
            print(f"   Role: {auth_user.role}")
        else:
            print(f"[ERROR] Django authentication FAILED!")
            print(f"   This is unexpected since password check passed")
            print(f"   Check if user.is_active = True")
            
            if not user.is_active:
                print(f"\n[WARN] User is inactive! Activating...")
                user.is_active = True
                user.save()
                print(f"[OK] User activated")
            
            return False
        
        # Test JWT token generation
        print(f"\n[*] Testing JWT token generation...")
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            print(f"[OK] JWT tokens generated successfully!")
            print(f"\n   Access Token (first 50 chars): {access_token[:50]}...")
            print(f"   Refresh Token (first 50 chars): {str(refresh)[:50]}...")
            
        except Exception as e:
            print(f"[ERROR] JWT token generation failed: {e}")
            return False
        
        # Summary
        print("\n" + "=" * 60)
        print("[SUCCESS] ADMIN USER VERIFICATION COMPLETE")
        print("=" * 60)
        print(f"\n[*] Login via Postman:")
        print(f"   POST http://localhost:8000/api/auth/login/")
        print(f"   {{")
        print(f'     "username": "{username}",')
        print(f'     "password": "{password}"')
        print(f"   }}")
        print(f"\n   Expected response: {{access: '...', refresh: '...'}}")
        print(f"\n[NOTE] Make sure Django server is running:")
        print(f"   python manage.py runserver")
        print()
        
        return True
        
    except User.DoesNotExist:
        print(f"[ERROR] User '{username}' not found in database!")
        print(f"\n[FIX] Create admin user:")
        print(f"   python create_admin.py")
        return False
    
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    try:
        success = verify_admin_user()
        if not success:
            print("\n[WARN] Verification failed! Check errors above.")
    except KeyboardInterrupt:
        print("\n\n[WARN] Cancelled")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
