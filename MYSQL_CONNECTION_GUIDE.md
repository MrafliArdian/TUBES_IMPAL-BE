# MySQL Database Connection Guide
# =================================

## Konfigurasi MySQL Saat Ini

Berdasarkan `settings.py`, Django dikonfigurasi untuk koneksi ke MySQL dengan detail:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kalkulator_db',
        'USER': 'kalku_user',
        'PASSWORD': 'Kalku123!',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

## Prasyarat

1. **MySQL Server** harus sudah terinstall dan running
2. **MySQL Connector Python** harus terinstall:
   ```bash
   pip install mysqlclient
   # atau jika error, gunakan:
   pip install pymysql
   ```

## Step-by-Step Setup MySQL

### 1. Check MySQL Service Running

**Windows:**
```powershell
# Check service status
Get-Service MySQL*

# Start MySQL service jika belum running
net start MySQL80    # atau MySQL57, sesuai versi Anda
```

**Via MySQL Workbench/phpMyAdmin:**
- Buka aplikasi dan coba connect

### 2. Login ke MySQL

```bash
mysql -u root -p
# Masukkan password root MySQL Anda
```

### 3. Create Database dan User

Di MySQL console, jalankan:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS kalkulator_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (jika belum ada)
CREATE USER IF NOT EXISTS 'kalku_user'@'localhost' IDENTIFIED BY 'Kalku123!';

-- Grant privileges
GRANT ALL PRIVILEGES ON kalkulator_db.* TO 'kalku_user'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;

-- Verify database created
SHOW DATABASES;

-- Exit MySQL
exit;
```

### 4. Test Koneksi dari Python

Buat file test `test_mysql_connection.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalkulatorInvestasi.settings')
django.setup()

from django.db import connection

def test_connection():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL Connection Successful!")
            print(f"   MySQL Version: {version[0]}")
            
            cursor.execute("SELECT DATABASE()")
            db = cursor.fetchone()
            print(f"   Current Database: {db[0]}")
            
            return True
    except Exception as e:
        print(f"❌ MySQL Connection Failed!")
        print(f"   Error: {e}")
        return False

if __name__ == '__main__':
    test_connection()
```

Jalankan:
```bash
python test_mysql_connection.py
```

## Troubleshooting

### Error: "Can't connect to MySQL server"

**Solusi:**
1. Pastikan MySQL service running
2. Check HOST dan PORT di settings.py
3. Coba ganti `HOST: '127.0.0.1'` menjadi `HOST: 'localhost'`

### Error: "Access denied for user"

**Solusi:**
1. Check username dan password di settings.py
2. Re-create user di MySQL:
   ```sql
   DROP USER IF EXISTS 'kalku_user'@'localhost';
   CREATE USER 'kalku_user'@'localhost' IDENTIFIED BY 'Kalku123!';
   GRANT ALL PRIVILEGES ON kalkulator_db.* TO 'kalku_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Error: "Unknown database"

**Solusi:**
```sql
CREATE DATABASE kalkulator_db;
```

### Error: "No module named 'MySQLdb'"

**Solusi:**
```bash
pip install mysqlclient

# Jika error di Windows, install pymysql:
pip install pymysql

# Lalu tambahkan di __init__.py atau settings.py:
import pymysql
pymysql.install_as_MySQLdb()
```

## Alternative: Update settings.py untuk pymysql

Jika menggunakan pymysql, tambahkan di `kalkulatorInvestasi/__init__.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

## Verify & Run Migrations

Setelah koneksi berhasil:

```bash
# 1. Test Django can connect
python manage.py check database

# 2. Run reset_database.py
python reset_database.py

# 3. Atau manual migrate
python manage.py migrate
```

## Quick Connection Test via Django Shell

```bash
python manage.py shell
```

```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SHOW TABLES")
print(cursor.fetchall())
```

## Common MySQL Commands

```sql
-- Show all databases
SHOW DATABASES;

-- Use specific database
USE kalkulator_db;

-- Show all tables
SHOW TABLES;

-- Show table structure
DESCRIBE accounts_customuser;

-- Show all users
SELECT User, Host FROM mysql.user;

-- Grant all privileges to user
GRANT ALL PRIVILEGES ON kalkulator_db.* TO 'kalku_user'@'localhost';
FLUSH PRIVILEGES;
```

## Summary Checklist

- [ ] MySQL service running
- [ ] Database `kalkulator_db` created
- [ ] User `kalku_user` created with correct password
- [ ] User granted privileges on database
- [ ] `mysqlclient` or `pymysql` installed
- [ ] Connection test successful
- [ ] Django migrations ready to run
