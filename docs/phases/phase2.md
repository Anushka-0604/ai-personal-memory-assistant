# Phase 2 – User Authentication & Database

## Status

✅ Completed

---

# Objective

Build the complete backend authentication system for the AI Personal Memory Assistant.

---

# Technologies Used

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT Authentication
- Passlib (bcrypt)
- Python-JOSE

---

# Features Implemented

## Backend

- FastAPI application structure
- Environment configuration
- PostgreSQL connection
- SQLAlchemy ORM
- Alembic database migrations

---

## User Management

- User model
- Password hashing
- User registration
- Duplicate email validation
- User login
- JWT token generation
- Protected API endpoint

---

## APIs

### GET /

Health check endpoint.

---

### POST /register

Registers a new user.

Request

```json
{
  "name": "Anushka",
  "email": "anushka@example.com",
  "password": "MyPassword123"
}
```

---

### POST /login

Authenticates a user.

Returns

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

---

### GET /me

Returns the authenticated user's profile.

Requires:

```
Authorization: Bearer <JWT>
```

---

# Database

Created:

- users table

Columns:

- id
- name
- email
- hashed_password

---

# Completed Milestones

- FastAPI setup
- PostgreSQL integration
- Alembic migrations
- User authentication
- JWT authentication
- Protected routes

---

# Next Phase

Phase 3 – AI Memory Engine