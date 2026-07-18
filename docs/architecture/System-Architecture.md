# System Architecture

## Overview

The AI Personal Memory & Decision Assistant is a production-level AI application designed to act as a secure digital second brain.

The system follows a layered architecture to ensure scalability, maintainability, modularity, and clean separation of concerns.

With the completion of **Phase 6**, the system supports Retrieval-Augmented Generation (RAG) with persistent conversation history, enabling context-aware, multi-turn AI conversations grounded in the user's stored memories.

---

# Current Architecture (Phase 6)

                          User
                            │
                            ▼
                     FastAPI Backend
                            │
      ┌─────────────────────┼────────────────────────────┐
      ▼                     ▼                            ▼
Authentication        Memory Service              Chat Service
      │                     │                            │
      ▼                     ▼                            ▼
JWT Verification      CRUD Operations          Conversation Management
      │                     │                            │
      │                     ▼                            ▼
      │             Embedding Service          Chat Session Service
      │                                              │
      │                                              ▼
      │                                      Chat Message Service
      │                                              │
      └──────────────┬───────────────────────────────┘
                     ▼
              SQLAlchemy ORM
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
 PostgreSQL + pgvector     Prompt Builder
         │                       │
         ▼                       ▼
 Semantic Search          Gemini LLM
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
- Chat Session Service
- Chat Message Service

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
- Chat Sessions
- Chat Messages
- Conversation History

---

# Current Database Schema

users
│
├──────────────► memories
│
└──────────────► chat_sessions
                    │
                    ▼
             chat_messages

Relationship

One User

↓

Many Memories

Each memory stores:

- Content
- Source
- Embedding Vector

Each chat session stores:

- Session Title
- User Relationship
- Conversation Metadata

Each chat message stores:

- User or Assistant Role
- Message Content
- Timestamp

---

# Request Flow (Memory CRUD)

Client

↓

POST /chat

↓

Authentication

↓

Chat Service

↓

Retrieve Conversation History

↓

Embedding Service

↓

Semantic Search (pgvector)

↓

Prompt Builder

↓

Gemini LLM

↓

Store Chat Messages

↓

AI Response
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
- Persistent Chat Sessions
- Conversation History
- Multi-turn Conversations
- Chat Session Management
- Chat Message Storage

---

# System Architecture Overview

                 React Frontend (Future)
                         │
                         ▼
                  FastAPI Backend
                         │
      ┌──────────────────┼────────────────────┐
      ▼                  ▼                    ▼
Authentication     Memory Service      Chat Service
      │                  │                    │
      ▼                  ▼                    ▼
 PostgreSQL       Embedding Service   Conversation History
      │                  │                    │
      └──────────────► pgvector ◄─────────────┘
                            │
                            ▼
                   Semantic Search
                            │
                            ▼
                     Prompt Builder
                            │
                            ▼
                      Gemini LLM
                            │
                            ▼
                 AI Generated Response

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


## Phase 7
- Automatic Memory Extraction
- Context Window Management
- Memory Ranking
- Memory Summarization
- Token Optimization

## Phase 8

- Document Intelligence
- Document Processing
- Chunking
- Document Embeddings
- Semantic Document Search

## Phase 9

- Voice Assistant
- Whisper Integration
- Voice Memories
- Voice Conversations

## Phase 10
- Decision Engine
- Personalized Recommendations
- Context-Aware Planning
- Knowledge Graph
- Multi-modal Memory

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

The system has evolved into a conversational Retrieval-Augmented Generation (RAG) powered AI assistant capable of maintaining persistent chat sessions and context-aware conversations.

The architecture now combines:

- Secure authentication
- Memory CRUD operations
- Semantic vector search
- Prompt engineering
- Gemini LLM integration
- AI-powered chat
- Conversation history
- Persistent chat sessions
- Multi-turn conversations

The modular service-oriented architecture ensures scalability, maintainability, and flexibility for future enhancements such as conversational memory, automatic memory extraction, intelligent decision support, and multi-modal AI capabilities.