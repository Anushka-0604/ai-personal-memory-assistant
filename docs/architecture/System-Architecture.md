# System Architecture

## Overview

The AI Personal Memory & Decision Assistant is a production-level AI application designed to act as a secure digital second brain.

The system follows a layered architecture to ensure scalability, maintainability, and clean separation of concerns.

---

# Current Architecture (Phase 3)

```
                    User
                      │
                      ▼
             FastAPI Backend
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Authentication              Memory Service
        │                           │
        ▼                           ▼
 JWT Verification           CRUD Operations
        │                           │
        └─────────────┬─────────────┘
                      ▼
               SQLAlchemy ORM
                      │
                      ▼
                 PostgreSQL
```

---

# Backend Layered Architecture

```
Client

↓

API Routes

↓

Services

↓

Database Layer

↓

PostgreSQL
```

---

# Backend Components

## API Layer

Responsible for:

- HTTP Endpoints
- Request Validation
- Response Models
- Dependency Injection

---

## Authentication Layer

Responsible for:

- User Registration
- User Login
- JWT Authentication
- OAuth2PasswordBearer
- Protected Endpoints

---

## Service Layer

Responsible for business logic.

Current Services

- Authentication
- Memory CRUD Operations

---

## Database Layer

Technology

- PostgreSQL
- SQLAlchemy ORM
- Alembic

Responsible for

- User Data
- Memory Storage
- Database Relationships

---

# Current Database Schema

```
users

│

└───────┐

        ▼

memories
```

Relationship

One User

↓

Many Memories

---

# Request Flow

```
Client

↓

FastAPI Route

↓

Authentication

↓

Memory Service

↓

SQLAlchemy ORM

↓

PostgreSQL

↓

Response
```

---

# Current Features

Implemented

- JWT Authentication
- OAuth2 Authorization
- User Registration
- User Login
- Memory CRUD APIs
- SQLAlchemy ORM
- Alembic Migrations
- Swagger Documentation

---

# Future AI Architecture

```
                React Frontend
                       │
                       ▼
                FastAPI Backend
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
 Authentication   Memory Service   AI Service
      │                │                │
      ▼                ▼                ▼
 PostgreSQL      PostgreSQL      Embeddings
      │                │                │
      └──────────────► pgvector ◄──────┘
                            │
                            ▼
                    Semantic Search
                            │
                            ▼
                    OpenAI / Gemini
                            │
                            ▼
                Personalized Response
```

---

# Future Components

Planned Features

- pgvector
- Vector Embeddings
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- OpenAI / Gemini
- Voice Assistant
- Whisper
- WebRTC
- Document Processing
- Image Memories
- Memory Timeline
- Knowledge Graph
- Decision Support

---

# Deployment

## Development

- Windows 11
- Python
- FastAPI
- PostgreSQL
- VS Code

## Production (Planned)

- React
- Docker
- AWS
- HTTPS
- pgvector
- OpenAI/Gemini