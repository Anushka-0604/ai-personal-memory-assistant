# Phase 2 API Documentation

## Endpoints

### GET /

Returns backend status.

---

### POST /register

Registers a user.

Request:

```json
{
    "name": "Anushka",
    "email": "anushka@example.com",
    "password": "MyPassword123"
}
```

---

### POST /login

Request

```
username
password
```

Response

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```

---

### GET /me

Headers

```
Authorization: Bearer <JWT>
```

Response

```json
{
    "id": 1,
    "name": "Anushka",
    "email": "anushka@example.com"
}
```