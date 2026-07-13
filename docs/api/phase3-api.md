# Phase 3 API Documentation

## Overview

Phase 3 introduces the Memory Engine of the AI Personal Memory & Decision Assistant.

Users can securely create, retrieve, update, and delete their personal memories.

All Memory APIs are protected using JWT Authentication through OAuth2PasswordBearer.

---

# Authentication

All endpoints in this phase require authentication.

Authenticate using the **Authorize** button available in Swagger UI.

---

# API Endpoints

## POST /memories

### Description

Creates a new memory for the authenticated user.

### Request Body

```json
{
    "content": "I like coffee.",
    "source": "chat"
}
```

### Success Response

```json
{
    "id": 1,
    "user_id": 1,
    "content": "I like coffee.",
    "source": "chat",
    "created_at": "2026-07-13T10:30:00",
    "updated_at": "2026-07-13T10:30:00"
}
```

Status Code

```
201 Created
```

---

## GET /memories

### Description

Returns all memories belonging to the authenticated user.

### Success Response

```json
[
    {
        "id": 1,
        "user_id": 1,
        "content": "I like coffee.",
        "source": "chat",
        "created_at": "2026-07-13T10:30:00",
        "updated_at": "2026-07-13T10:30:00"
    }
]
```

Status Code

```
200 OK
```

---

## GET /memories/{id}

### Description

Returns a single memory using its ID.

### Success Response

```json
{
    "id": 1,
    "user_id": 1,
    "content": "I like coffee.",
    "source": "chat",
    "created_at": "2026-07-13T10:30:00",
    "updated_at": "2026-07-13T10:30:00"
}
```

Possible Errors

```
404 Not Found
```

---

## PUT /memories/{id}

### Description

Updates an existing memory.

### Request Body

```json
{
    "content": "I like coffee and tea.",
    "source": "chat"
}
```

### Success Response

Returns the updated memory.

Status Code

```
200 OK
```

Possible Errors

```
404 Not Found
```

---

## DELETE /memories/{id}

### Description

Deletes a memory.

Status Code

```
204 No Content
```

Possible Errors

```
404 Not Found
```

---

# HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Successful Request |
| 201 | Resource Created |
| 204 | Resource Deleted Successfully |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Resource Not Found |

---

# Phase 3 Summary

Implemented:

- Memory CRUD APIs
- JWT Protected Endpoints
- OAuth2 Authentication
- Memory Service Layer
- User-specific Memory Access
- RESTful API Design