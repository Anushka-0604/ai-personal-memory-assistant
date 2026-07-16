# System Architecture

## Overview

The AI Personal Memory & Decision Assistant is a production-level AI application designed to act as a secure digital second brain.

The system follows a layered architecture to ensure scalability, maintainability, modularity, and clean separation of concerns.

With the completion of **Phase 5**, the system now supports Retrieval-Augmented Generation (RAG), enabling AI-generated responses grounded in the user's stored memories.

---

# Current Architecture (Phase 5)

```
                          User
                            │
                            ▼
                     FastAPI Backend
                            │
      ┌─────────────────────┼─────────────────────┐
      ▼                     ▼                     ▼
Authentication        Memory Service         Chat Service
      │                     │                     │
      ▼                     ▼                     ▼
JWT Verification      CRUD Operations      RAG Pipeline
      │                     │                     │
      └──────────────┬──────┴──────────────┐
                     ▼                     ▼
             SQLAlchemy ORM         Prompt Builder
                     │                     │
                     ▼                     ▼
                PostgreSQL          Gemini LLM
                     │
                     ▼
                 pgvector
```

---

# Backend Layered Architecture

```
Client

↓

API Routes

↓

Business Services

↓

Database Layer

↓

PostgreSQL + pgvector
```

---

# Backend Components

## API Layer

Responsible for:

- HTTP Endpoints
- Request Validation
- Response Models
- Dependency Injection
- JWT-Protected APIs

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

- Authentication Service
- Memory Service
- Embedding Service
- Prompt Builder
- LLM Service
- Chat Service

---

## Database Layer

Technology

- PostgreSQL
- SQLAlchemy ORM
- Alembic
- pgvector

Responsible for:

- User Data
- Memory Storage
- Vector Embeddings
- Semantic Search

---

# Current Database Schema

```
users

│

└──────────────┐

               ▼

           memories
```

Relationship

One User

↓

Many Memories

Each memory stores:

- Content
- Source
- Embedding Vector

---

# Request Flow (Memory CRUD)

```
Client

↓

FastAPI Route

↓

Authentication

↓

Memory Service

↓

Embedding Service

↓

SQLAlchemy ORM

↓

PostgreSQL

↓

Response
```

---

# Request Flow (AI Chat)

```
Client

↓

POST /chat

↓

Authentication

↓

Chat Service

↓

Embedding Service

↓

Semantic Search (pgvector)

↓

Prompt Builder

↓

Gemini LLM

↓

AI Response
```

---

# Current Features

Implemented

- JWT Authentication
- OAuth2 Authorization
- User Registration
- User Login
- Memory CRUD APIs
- Automatic Embedding Generation
- pgvector Integration
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- Gemini LLM Integration
- AI Chat Endpoint
- SQLAlchemy ORM
- Alembic Migrations
- Swagger Documentation
- Logging
- Graceful Error Handling

---

# System Architecture Overview

```
                 React Frontend (Future)
                         │
                         ▼
                  FastAPI Backend
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
Authentication     Memory Service     Chat Service
      │                  │                  │
      ▼                  ▼                  ▼
 PostgreSQL       Embedding Service   Prompt Builder
      │                  │                  │
      └──────────────► pgvector ◄───────────┘
                            │
                            ▼
                   Semantic Search
                            │
                            ▼
                      Gemini LLM
                            │
                            ▼
                 AI Generated Response
```

---

# Current Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic

## Database

- PostgreSQL
- pgvector

## Artificial Intelligence

- Sentence Transformers
- all-MiniLM-L6-v2
- Google Gemini API
- Retrieval-Augmented Generation (RAG)

## Security

- JWT Authentication
- OAuth2PasswordBearer
- Password Hashing (bcrypt)

---

# Future Components

Planned Features

## Phase 6

- Conversation History
- Automatic Memory Extraction
- Session-Based Conversations
- Short-Term Conversational Memory

## Phase 7

- Context Window Management
- Memory Ranking
- Memory Summarization
- Token Optimization

## Phase 8

- Decision Engine
- Personalized Recommendations
- Context-Aware Planning

## Phase 9

- Voice Assistant
- Whisper Integration
- WebRTC
- Image Memories
- Document Processing
- Multi-modal Memory
- Knowledge Graph

---

# Deployment

## Development

- Windows 11
- Python
- FastAPI
- PostgreSQL
- pgvector
- VS Code

## Production (Planned)

- React
- Docker
- AWS
- HTTPS
- PostgreSQL
- pgvector
- Google Gemini / OpenAI
- Nginx
- CI/CD Pipeline

---

# Summary

The system has evolved from a secure memory management backend into a Retrieval-Augmented Generation (RAG) powered AI assistant.

The architecture now combines:

- Secure authentication
- Memory CRUD operations
- Semantic vector search
- Prompt engineering
- Gemini LLM integration
- AI-powered chat

The modular service-oriented architecture ensures scalability, maintainability, and flexibility for future enhancements such as conversational memory, automatic memory extraction, intelligent decision support, and multi-modal AI capabilities.