#!/usr/bin/env python
"""
Test MySQL Database Connection
================================
Script untuk test koneksi ke MySQL database.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalkulatorInvestasi.settings')
django.setup()

from django.db import connection
from django.conf import settings

def test_mysql_connection():
    """Test MySQL database connection"""
    
    print("=" * 60)
    print("  MYSQL CONNECTION TEST")
    print("=" * 60)
    
    # Show config
    db_config = settings.DATABASES['default']
    print(f"\n📋 Database Configuration:")
    print(f"   Engine: {db_config['ENGINE']}")
    print(f"   Database: {db_config['NAME']}")
    print(f"   User: {db_config['USER']}")
    print(f"   Host: {db_config['HOST']}")
    print(f"   Port: {db_config['PORT']}")
    
    # Test connection
    print(f"\n🔌 Testing connection...")
    try:
        with connection.cursor() as cursor:
            # Get MySQL version
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"\n✅ MySQL Connection Successful!")
            print(f"   MySQL Version: {version[0]}")
            
            # Get current database
            cursor.execute("SELECT DATABASE()")
            db = cursor.fetchone()
            print(f"   Current Database: {db[0]}")
            
            # Show tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"\n📊 Existing tables ({len(tables)}):")
                for (table,) in tables:
                    print(f"   - {table}")
            else:
                print(f"\n⚠️  No tables found (database is empty)")
                print(f"   Run migrations: python reset_database.py")
            
            # Check django_migrations table
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = %s AND table_name = 'django_migrations'
            """, [db_config['NAME']])
            
            has_migrations = cursor.fetchone()[0] > 0
            
            if has_migrations:
                cursor.execute("SELECT COUNT(*) FROM django_migrations")
                migration_count = cursor.fetchone()[0]
                print(f"\n📝 Migration records: {migration_count}")
            else:
                print(f"\n⚠️  No migration table found")
                print(f"   Database needs to be initialized")
            
        print("\n" + "=" * 60)
        print("✅ CONNECTION TEST PASSED")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("   1. Run: python reset_database.py")
        print("   2. Run: python manage.py runserver")
        print("\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ MySQL Connection Failed!")
        print(f"   Error: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Check if MySQL service is running")
        print(f"   2. Verify database 'kalkulator_db' exists")
        print(f"   3. Verify user 'kalku_user' has correct password")
        print(f"   4. Check MySQL port (usually 3306)")
        print(f"\n📖 See MYSQL_CONNECTION_GUIDE.md for detailed setup")
        
        return False

if __name__ == '__main__':
    try:
        success = test_mysql_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
