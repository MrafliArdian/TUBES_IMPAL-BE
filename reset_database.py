"""
Database Reset & Migration Script
==================================
Script untuk membersihkan dan setup ulang database dengan CustomUser model.
Gunakan ini jika ada masalah dengan migration atau CustomUser.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalkulatorInvestasi.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def reset_database():
    """Reset database dan apply migrations dari awal"""
    
    print("=" * 60)
    print("  DATABASE RESET & MIGRATION SCRIPT")
    print("=" * 60)
    
    # Step 1: Clear migration history
    print("\n📋 Step 1: Clearing migration history...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations")
            print("✅ Migration history cleared")
    except Exception as e:
        print(f"⚠️  Could not clear migrations: {e}")
        print("   (This is OK if database is fresh)")
    
    # Step 2: Drop all tables
    print("\n🗑️  Step 2: Dropping all tables...")
    try:
        with connection.cursor() as cursor:
            # Get all tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE()
            """)
            tables = cursor.fetchall()
            
            # Disable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Drop each table
            for (table_name,) in tables:
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
                print(f"   ✓ Dropped table: {table_name}")
            
            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            print("✅ All tables dropped")
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        return False
    
    # Step 3: Run migrations
    print("\n🔧 Step 3: Running migrations...")
    try:
        call_command('migrate', verbosity=2)
        print("✅ Migrations applied successfully")
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
        return False
    
    # Step 4: Verify CustomUser model
    print("\n✅ Step 4: Verifying CustomUser model...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        print(f"   Model: {User.__name__}")
        print(f"   Table: {User._meta.db_table}")
        
        # Check fields
        custom_fields = ['role', 'full_name', 'phone_number']
        model_fields = [f.name for f in User._meta.get_fields()]
        
        print("   Custom fields:")
        for field in custom_fields:
            if field in model_fields:
                print(f"      ✓ {field}")
            else:
                print(f"      ✗ {field} (MISSING!)")
        
        print("✅ CustomUser model verified")
        
    except Exception as e:
        print(f"❌ Error verifying model: {e}")
        return False
    
    # Step 5: Create admin user (optional)
    print("\n👤 Step 5: Would you like to create an admin user?")
    print("   You can do this later with: python manage.py createsuperuser")
    print("   Or via the create_admin.py script")
    
    print("\n" + "=" * 60)
    print("✅ DATABASE RESET COMPLETE!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Restart Django server: python manage.py runserver")
    print("   2. Test registration: POST /api/auth/register/")
    print("   3. Create admin user if needed")
    print("\n")
    
    return True

if __name__ == '__main__':
    try:
        success = reset_database()
        if success:
            print("🎉 Success! Database is ready to use.")
            sys.exit(0)
        else:
            print("❌ Database reset failed. Check errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
