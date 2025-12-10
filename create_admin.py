"""
Quick Create Admin User Script
================================
Script untuk membuat admin user dengan mudah.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalkulatorInvestasi.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    """Create admin user interactively"""
    
    print("=" * 60)
    print("  CREATE ADMIN USER")
    print("=" * 60)
    
    # Get input
    username = input("\nUsername (default: admin): ").strip() or "admin"
    email = input("Email (default: admin@example.com): ").strip() or "admin@example.com"
    password = input("Password (default: AdminPass123!): ").strip() or "AdminPass123!"
    full_name = input("Full Name (default: Administrator): ").strip() or "Administrator"
    
    # Check if user exists
    if User.objects.filter(username=username).exists():
        print(f"\n⚠️  User '{username}' already exists!")
        update = input("Update to ADMIN role? (y/n): ").strip().lower()
        if update == 'y':
            user = User.objects.get(username=username)
            user.role = 'ADMIN'
            user.save()
            print(f"✅ {username} updated to ADMIN role")
        return
    
    # Create admin user
    try:
        admin = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            role='ADMIN'
        )
        
        print(f"\n✅ Admin user created successfully!")
        print(f"\n   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Role: {admin.get_role_display()}")
        print(f"\n📝 Login credentials:")
        print(f"   POST /api/auth/login/")
        print(f"   {{")
        print(f'     "username": "{username}",')
        print(f'     "password": "{password}"')
        print(f"   }}")
        
    except Exception as e:
        print(f"\n❌ Error creating admin: {e}")

if __name__ == '__main__':
    try:
        create_admin()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
