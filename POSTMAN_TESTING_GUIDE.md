# Postman Testing Guide - Investment Calculator API

Panduan lengkap untuk testing API menggunakan Postman.

## Persiapan

1. **Start Django Server**
   ```bash
   python manage.py runserver
   ```
   
2. **Base URL**: `http://localhost:8000` atau `http://127.0.0.1:8000`

---

## 1. Register User Baru

**Endpoint**: `POST /api/auth/register/`  
**Authorization**: None (Public)

### Request Body (JSON):
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "TestPass123!",
  "password2": "TestPass123!",
  "full_name": "Test User",
  "phone_number": "08123456789"
}
```

### Expected Response (201 Created):
```json
{
  "message": "User berhasil dibuat",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "phone_number": "08123456789",
    "role": "USER",
    "date_joined": "2024-12-10T15:00:00Z"
  }
}
```

---

## 2. Login & Get JWT Token

**Endpoint**: `POST /api/auth/login/`  
**Authorization**: None (Public)

### Request Body (JSON):
```json
{
  "username": "testuser",
  "password": "TestPass123!"
}
```

### Expected Response (200 OK):
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 🔑 **PENTING**: Copy `access` token untuk request selanjutnya!

---

## 3. Setup Authorization di Postman

Untuk semua endpoint yang memerlukan authentication:

1. **Tab "Authorization"**
2. **Type**: Bearer Token
3. **Token**: Paste access token dari response login

Atau di Headers:
- **Key**: `Authorization`
- **Value**: `Bearer <access_token>`

---

## 4. Test User Info (Me)

**Endpoint**: `GET /api/auth/me/`  
**Authorization**: Bearer Token (Required)

### Expected Response (200 OK):
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "phone_number": "08123456789",
  "role": "USER",
  "date_joined": "2024-12-10T15:00:00Z"
}
```

---

## 5. Create Admin User

### Via Django Shell:
```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Create admin user
admin = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='AdminPass123!',
    full_name='Administrator',
    role='ADMIN'
)
print(f"Admin created: {admin.username}")
```

### Atau via Django Admin:
```bash
python manage.py createsuperuser
# Kemudian login ke /admin/ dan ubah role menjadi ADMIN
```

---

## 6. Admin Endpoints Testing

**⚠️ PENTING**: Login sebagai admin dulu untuk mendapatkan admin token!

### 6.1 List All Users

**Endpoint**: `GET /api/auth/admin/users/`  
**Authorization**: Bearer Token (Admin Required)

**Query Parameters** (Optional):
- `role=USER` atau `role=ADMIN` - Filter by role
- `search=test` - Search by username, email, atau full_name

#### Example Request:
```
GET http://localhost:8000/api/auth/admin/users/
```

#### Example with Filter:
```
GET http://localhost:8000/api/auth/admin/users/?role=USER&search=test
```

#### Expected Response (200 OK):
```json
{
  "count": 2,
  "users": [
    {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "full_name": "Test User",
      "phone_number": "08123456789",
      "role": "USER",
      "is_active": true,
      "date_joined": "2024-12-10T15:00:00Z",
      "last_login": "2024-12-10T15:30:00Z",
      "total_calculations": 5
    }
  ]
}
```

### 6.2 View User Detail

**Endpoint**: `GET /api/auth/admin/users/<user_id>/`  
**Authorization**: Bearer Token (Admin Required)

#### Example Request:
```
GET http://localhost:8000/api/auth/admin/users/1/
```

#### Expected Response (200 OK):
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "phone_number": "08123456789",
  "role": "USER",
  "is_active": true,
  "date_joined": "2024-12-10T15:00:00Z",
  "last_login": "2024-12-10T15:30:00Z",
  "total_calculations": 5
}
```

### 6.3 View User Calculation History

**Endpoint**: `GET /api/auth/admin/users/<user_id>/history/`  
**Authorization**: Bearer Token (Admin Required)

**Query Parameters** (Optional):
- `calculator_type=emergency_fund` - Filter by calculator type
- `calculator_type=pension` - Pension calculations
- `calculator_type=gold` - Gold calculations

#### Example Request:
```
GET http://localhost:8000/api/auth/admin/users/1/history/
```

#### Expected Response (200 OK):
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "phone_number": "08123456789",
    "role": "USER",
    "date_joined": "2024-12-10T15:00:00Z"
  },
  "calculations": {
    "emergency_fund": [...],
    "pension": [...],
    "gold": [...]
  }
}
```

---

## 7. Calculator Endpoints Testing

### 7.1 Dana Darurat (Emergency Fund)

**Endpoint**: `POST /api/dana-darurat/`  
**Authorization**: Bearer Token (Required)

#### Request Body (JSON):
```json
{
  "monthly_expense": 5000000,
  "months_to_save": 12,
  "current_emergency_fund": 10000000,
  "monthly_invest": 2000000,
  "expected_return_pct": 8.0
}
```

#### Expected Response (201 Created):
```json
{
  "id": 1,
  "user": 1,
  "monthly_expense": "5000000.00",
  "months_to_save": 12,
  "current_emergency_fund": "10000000.00",
  "monthly_invest": "2000000.00",
  "expected_return_pct": "8.00",
  "needed_fund": "60000000.00",
  "future_value": "36254789.50",
  "gap_amount": "-23745210.50",
  "status": "tidak cukup",
  "recommendation": "Dana darurat Anda masih kurang. Target kebutuhan adalah Rp 60,000,000, namun dengan investasi saat ini hanya akan terkumpul Rp 36,254,789. Kekurangan: Rp 23,745,210. Pertimbangkan untuk menambah investasi bulanan sekitar Rp 1,978,767 atau perpanjang waktu pengumpulan dana darurat Anda.",
  "is_suitable": false,
  "created_at": "2024-12-10T15:45:00Z"
}
```

#### Get List Dana Darurat:
```
GET http://localhost:8000/api/dana-darurat/
```

### 7.2 Dana Pensiun (Pension)

**Endpoint**: `POST /api/dana-pensiun/`  
**Authorization**: Bearer Token (Required)

#### Request Body (JSON):
```json
{
  "current_age": 30,
  "retire_age": 55,
  "monthly_expense_now": 8000000,
  "inflation_pct": 5.0,
  "expected_return_pct": 10.0,
  "pension_years": 20,
  "monthly_invest": 3000000
}
```

#### Expected Response (201 Created):
```json
{
  "id": 1,
  "user": 1,
  "current_age": 30,
  "retire_age": 55,
  "monthly_expense_now": "8000000.00",
  "inflation_pct": "5.00",
  "expected_return_pct": "10.00",
  "pension_years": 20,
  "monthly_invest": "3000000.00",
  "total_need_at_retire": "5000000000.00",
  "estimated_portfolio": "3500000000.00",
  "status": "tidak cukup",
  "recommendation": "Dana pensiun Anda masih kurang. Target kebutuhan untuk 20 tahun pensiun adalah Rp 5,000,000,000, namun dengan investasi saat ini hanya akan terkumpul Rp 3,500,000,000. Kekurangan: Rp 1,500,000,000. Pertimbangkan untuk menambah investasi bulanan sekitar Rp 5,000,000 atau memperpanjang masa kerja sebelum pensiun.",
  "is_suitable": false,
  "created_at": "2024-12-10T15:50:00Z"
}
```

### 7.3 Kalkulator Emas (Gold)

**Endpoint**: `POST /api/emas/`  
**Authorization**: Bearer Token (Required)

#### Request Body (JSON) - Emas ke Rupiah:
```json
{
  "mode": "emas_to_rupiah",
  "price_choice": "BUY",
  "grams_input": 10,
  "price_per_gram": 1050000
}
```

#### Request Body (JSON) - Rupiah ke Emas:
```json
{
  "mode": "rupiah_to_emas",
  "price_choice": "SELL",
  "rupiah_input": 10000000,
  "price_per_gram": 1040000
}
```

---

## 8. Unified History Endpoints

### 8.1 Get All History

**Endpoint**: `GET /api/history/`  
**Authorization**: Bearer Token (Required)

**Query Parameters** (Optional):
- `calculator_type=emergency_fund` - Filter by type
- `date_from=2024-01-01` - Filter dari tanggal
- `date_to=2024-12-31` - Filter sampai tanggal
- `sort=newest` atau `sort=oldest` - Sorting

#### Example Request:
```
GET http://localhost:8000/api/history/
```

#### Example with Filters:
```
GET http://localhost:8000/api/history/?calculator_type=emergency_fund&sort=newest
```

#### Expected Response (200 OK):
```json
{
  "count": 3,
  "history": [
    {
      "id": 1,
      "calculator_type": "emergency_fund",
      "calculator_name": "Dana Darurat",
      "date": "2024-12-10T15:45:00Z",
      "status": "tidak cukup",
      "is_suitable": false,
      "summary": "Target: Rp 60,000,000, Estimasi: Rp 36,254,789",
      "recommendation": "Dana darurat Anda masih kurang..."
    },
    {
      "id": 2,
      "calculator_type": "pension",
      "calculator_name": "Dana Pensiun",
      "date": "2024-12-10T15:50:00Z",
      "status": "cukup",
      "is_suitable": true,
      "summary": "Kebutuhan: Rp 5,000,000,000, Estimasi: Rp 6,000,000,000",
      "recommendation": "Selamat! Persiapan pensiun Anda sudah mencukupi..."
    }
  ]
}
```

### 8.2 Get History by Calculator Type

**Endpoint**: `GET /api/history/<calculator_type>/`  
**Authorization**: Bearer Token (Required)

#### Example Requests:
```
GET http://localhost:8000/api/history/emergency_fund/
GET http://localhost:8000/api/history/pension/
GET http://localhost:8000/api/history/gold/
```

---

## 9. Common Error Responses

### 401 Unauthorized (No Token)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 401 Unauthorized (Invalid/Expired Token)
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

**Solution**: Login ulang untuk mendapatkan token baru

### 403 Forbidden (Not Admin)
```json
{
  "detail": "Anda tidak memiliki akses admin. Hanya admin yang bisa mengakses endpoint ini."
}
```

**Solution**: Login dengan akun admin

### 400 Bad Request
```json
{
  "password": ["Password dan konfirmasi tidak sama."]
}
```

---

## 10. Postman Collection Setup (Optional)

### Variables untuk Postman Environment:

1. Create New Environment: "Investment Calculator Dev"
2. Add Variables:
   - `base_url`: `http://localhost:8000`
   - `access_token`: (kosong, akan di-set otomatis)
   - `user_id`: (kosong, untuk testing)

### Auto-set Token Script:

Di tab **Tests** untuk Login request, tambahkan:

```javascript
// Auto-save access token
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
    console.log("Token saved!");
}
```

### Authorization di Collection Level:

1. Click Collection → Authorization
2. Type: Bearer Token
3. Token: `{{access_token}}`

Sekarang semua request di collection akan otomatis menggunakan token!

---

## 11. Testing Flow Example

### Complete Testing Flow:

1. **Register User**
   - `POST /api/auth/register/` dengan data user baru

2. **Login**
   - `POST /api/auth/login/` dengan credentials
   - Copy access token

3. **Test User Info**
   - `GET /api/auth/me/` dengan Bearer token

4. **Create Calculations**
   - `POST /api/dana-darurat/` dengan data
   - `POST /api/dana-pensiun/` dengan data
   - `POST /api/emas/` dengan data

5. **View History**
   - `GET /api/history/` untuk semua history
   - `GET /api/history/emergency_fund/` untuk filter

6. **Create Admin & Test Admin Endpoints**
   - Create admin via shell
   - Login sebagai admin
   - `GET /api/auth/admin/users/`
   - `GET /api/auth/admin/users/1/history/`

---

## Tips & Troubleshooting

### Token Expired?
```bash
# Refresh token
POST /api/auth/refresh/
{
  "refresh": "<your_refresh_token>"
}
```

### Can't Access Admin Endpoints?
1. Check user role di database atau `/api/auth/me/`
2. Pastikan role = "ADMIN"
3. Login ulang untuk refresh token

### CORS Error?
Check `CORS_ALLOWED_ORIGINS` di `settings.py`

### Server Not Running?
```bash
python manage.py runserver
```

---

Happy Testing! 🚀
