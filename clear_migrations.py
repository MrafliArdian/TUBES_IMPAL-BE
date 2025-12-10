#!/usr/bin/env python
"""
Script untuk membersihkan migration history dari database.
Gunakan ini jika terjadi InconsistentMigrationHistory error.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalkulatorInvestasi.settings')
django.setup()

from django.db import connection

def clear_migration_history():
    """Clear all migration history from django_migrations table"""
    with connection.cursor() as cursor:
        print("🗑️  Clearing migration history...")
        
        # Delete all migration records
        cursor.execute("DELETE FROM django_migrations")
        deleted_count = cursor.rowcount
        
        print(f"✅ Deleted {deleted_count} migration records")
        print("\n📋 Migration history cleared!")
        print("\nSekarang jalankan:")
        print("  python manage.py migrate --fake-initial")
        print("\nAtau jika masih error:")
        print("  python manage.py migrate")

if __name__ == '__main__':
    try:
        clear_migration_history()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nJika error, coba manual via MySQL:")
        print("  mysql -u kalku_user -p")
        print("  USE kalkulator_db;")
        print("  DELETE FROM django_migrations;")
        print("  exit;")
