# Authentication Documentation

The AI Personal Memory & Decision Assistant uses **JWT (JSON Web Tokens)** with **OAuth2 Password Flow** for user authentication.

Authentication ensures that only registered users can access their own memories and protected API endpoints.

---

# Authentication Technologies

- JWT (JSON Web Token)
- OAuth2PasswordBearer
- Passlib (bcrypt)
- Python-JOSE

---

# User Registration

## Endpoint

```
POST /register
```

### Description

Creates a new user account.

### Request Body

```json
{
    "name": "Anushka",
    "email": "anushka@gmail.com",
    "password": "password123"
}
```

### Success Response

```json
{
    "message": "User registered successfully!"
}
```

---

# User Login

## Endpoint

```
POST /login
```

### Description

Authenticates a user and returns a JWT access token.

### Request

Uses **OAuth2 Password Form**.

Fields:

- username (email)
- password

### Success Response

```json
{
    "access_token": "<JWT_TOKEN>",
    "token_type": "bearer"
}
```

---

# Protected APIs

The following endpoints require authentication:

- GET /me
- POST /memories
- GET /memories
- GET /memories/{id}
- PUT /memories/{id}
- DELETE /memories/{id}

---

# Swagger Authentication

The project uses **OAuth2PasswordBearer**, allowing Swagger UI to authenticate users directly.

### Steps

1. Login using the **Authorize** button.
2. Enter:
   - Username (Email)
   - Password
3. Click **Authorize**.
4. Swagger automatically includes the JWT token in all protected requests.

No manual Authorization header is required.

---

# Password Hashing

Passwords are never stored in plain text.

The application uses:

- bcrypt
- Passlib CryptContext

Before storing a password:

```
User Password
        │
        ▼
bcrypt Hash
        │
        ▼
Stored in PostgreSQL
```

---

# JWT Token

Each token contains:

- User email (subject)
- Expiration time

Example payload:

```json
{
    "sub": "anushka@gmail.com",
    "exp": 1752500000
}
```

---

# Authentication Flow

```
User
 │
 ▼
Register
 │
 ▼
Password Hashed (bcrypt)
 │
 ▼
Stored in PostgreSQL
 │
 ▼
Login
 │
 ▼
Credentials Verified
 │
 ▼
JWT Generated
 │
 ▼
Swagger / Client Stores Token
 │
 ▼
Protected API Request
 │
 ▼
OAuth2PasswordBearer
 │
 ▼
JWT Verification
 │
 ▼
Current User Retrieved
 │
 ▼
Response Returned
```

---

# Security Features

- JWT Authentication
- OAuth2 Password Flow
- Password Hashing using bcrypt
- User-specific resource access
- Protected Memory APIs
- Unauthorized requests return **401 Unauthorized**