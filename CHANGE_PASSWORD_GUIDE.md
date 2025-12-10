# Change Password & Update Profile - Testing Guide

## Overview

Fitur yang sudah ditambahkan:
1. ✅ **Change Password** - User bisa ganti password dengan verifikasi password lama
2. ✅ **Update Profile** - User bisa update email, full_name, phone_number
3. ✅ **Username Immutable** - Username TIDAK BISA diubah (read-only)

---

## 1. Change Password

**Endpoint**: `POST /api/auth/change-password/`  
**Authorization**: Bearer Token (Required)

### Request Body:
```json
{
  "old_password": "TestPass123!",
  "new_password": "NewPass123!",
  "new_password2": "NewPass123!"
}
```

### Success Response (200 OK):
```json
{
  "message": "Password berhasil diubah",
  "detail": "Silakan login ulang dengan password baru"
}
```

### Error Responses:

**Old password salah (400 Bad Request):**
```json
{
  "old_password": ["Password lama salah."]
}
```

**New password tidak sama (400 Bad Request):**
```json
{
  "new_password": ["Password baru tidak sama."]
}
```

**New password terlalu lemah (400 Bad Request):**
```json
{
  "new_password": ["This password is too common."]
}
```

### Testing Flow:

1. **Login untuk dapat token:**
```
POST http://localhost:8000/api/auth/login/
{
  "username": "testuser",
  "password": "TestPass123!"
}
```

2. **Change password:**
```
POST http://localhost:8000/api/auth/change-password/
Authorization: Bearer <access_token>

Body:
{
  "old_password": "TestPass123!",
  "new_password": "NewPassword456!",
  "new_password2": "NewPassword456!"
}
```

3. **Login ulang dengan password baru:**
```
POST http://localhost:8000/api/auth/login/
{
  "username": "testuser",
  "password": "NewPassword456!"
}
```

---

## 2. Update Profile

**Endpoint**: `GET/PUT/PATCH /api/auth/profile/`  
**Authorization**: Bearer Token (Required)

### GET - View Profile

```
GET http://localhost:8000/api/auth/profile/
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "phone_number": "08123456789",
  "role": "USER",
  "date_joined": "2024-12-10T10:00:00Z"
}
```

### PUT - Update Full Profile

Update semua field sekaligus (kecuali username dan role):

```
PUT http://localhost:8000/api/auth/profile/
Authorization: Bearer <access_token>

Body:
{
  "email": "newemail@example.com",
  "full_name": "New Full Name",
  "phone_number": "08987654321"
}
```

**Response (200 OK):**
```json
{
  "message": "Profile berhasil diupdate",
  "user": {
    "id": 1,
    "username": "testuser",  // USERNAME TETAP (tidak berubah)
    "email": "newemail@example.com",
    "full_name": "New Full Name",
    "phone_number": "08987654321",
    "role": "USER",
    "date_joined": "2024-12-10T10:00:00Z"
  }
}
```

### PATCH - Update Partial Profile

Update hanya beberapa field saja:

```
PATCH http://localhost:8000/api/auth/profile/
Authorization: Bearer <access_token>

Body:
{
  "email": "updatedemail@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "Profile berhasil diupdate",
  "user": {
    "id": 1,
    "username": "testuser",  // Tetap tidak berubah
    "email": "updatedemail@example.com",  // Hanya email yang berubah
    "full_name": "New Full Name",  // Tetap
    "phone_number": "08987654321",  // Tetap
    "role": "USER",
    "date_joined": "2024-12-10T10:00:00Z"
  }
}
```

---

## 3. Username Immutability Test

### Test 1: Try to Change Username via Profile Update

```
PATCH http://localhost:8000/api/auth/profile/
Authorization: Bearer <access_token>

Body:
{
  "username": "newusername",  // INI AKAN DIABAIKAN
  "email": "test@example.com"
}
```

**Result**: Username akan tetap sama (read-only), hanya email yang update.

### Test 2: Verify Username Tidak Berubah

```
GET http://localhost:8000/api/auth/me/

Response:
{
  "username": "testuser",  // TETAP TIDAK BERUBAH
  ...
}
```

---

## Complete Testing Scenario

### Scenario 1: Update Profile & Change Password

```bash
# 1. Login
POST /api/auth/login/
{
  "username": "testuser",
  "password": "TestPass123!"
}

# 2. View current profile
GET /api/auth/profile/
Authorization: Bearer <token>

# 3. Update profile (email, phone)
PATCH /api/auth/profile/
Authorization: Bearer <token>
{
  "email": "updated@example.com",
  "phone_number": "08111222333"
}

# 4. Change password
POST /api/auth/change-password/
Authorization: Bearer <token>
{
  "old_password": "TestPass123!",
  "new_password": "NewSecure123!",
  "new_password2": "NewSecure123!"
}

# 5. Login with new password
POST /api/auth/login/
{
  "username": "testuser",  // Username tetap sama
  "password": "NewSecure123!"  // Password baru
}

# 6. Verify profile updated
GET /api/auth/me/
```

---

## Security Features

✅ **Password Change Requires Old Password**
- Mencegah unauthorized password changes
- Jika ada penyusup dengan token, tidak bisa ganti password tanpa tahu password lama

✅ **Password Validation**
- Django's built-in password validators aktif
- Minimum length, common password check, etc.

✅ **Username Immutable**
- Username tidak bisa diubah setelah registrasi
- Menjaga konsistensi data dan referential integrity

✅ **Role Protection**
- User tidak bisa mengubah role sendiri
- Hanya admin via Django admin yang bisa ubah role

---

## API Endpoints Summary

### User Profile Management (Authenticated)
- `GET /api/auth/me/` - Get current user info
- `GET /api/auth/profile/` - View profile
- `PUT /api/auth/profile/` - Update full profile
- `PATCH /api/auth/profile/` - Update partial profile
- `POST /api/auth/change-password/` - Change password

### Fields Access Control
- **Editable**: email, full_name, phone_number
- **Read-Only**: username, role, id, date_joined
- **Secret**: password (via change-password endpoint only)

---

## Error Handling

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```
**Solution**: Login dan gunakan Bearer token

### 400 Bad Request
```json
{
  "email": ["Enter a valid email address."]
}
```
**Solution**: Perbaiki format data

### Token Expired
```json
{
  "detail": "Given token not valid for any token type"
}
```
**Solution**: Login ulang untuk mendapat token baru

---

## Notes

- Setelah change password, JWT token lama masih valid sampai expired
- Untuk security maksimal, bisa logout semua session setelah change password (optional feature)
- Username case-sensitive dan harus unique
- Email tidak wajib unique (bisa sama untuk multiple users)
