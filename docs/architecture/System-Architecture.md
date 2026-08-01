# System Architecture

## Overview

The AI Personal Memory & Decision Assistant is a production-level AI application designed to act as a secure digital second brain.

The system follows a layered architecture to ensure scalability, maintainability, modularity, and clean separation of concerns.

With the completion of **Phase 7**, the system has evolved into a production-grade intelligent memory platform supporting automatic memory understanding, hybrid retrieval, long-term memory management, knowledge graph construction, personalized retrieval, Retrieval-Augmented Generation (RAG), AI observability, and analytics.

---

# Current Architecture (Phase 7)

```
                           User
                             │
                             ▼
                      FastAPI Backend
                             │
        ┌────────────────────┼──────────────────────────────┐
        ▼                    ▼                              ▼
 Authentication       Memory Service                 Chat Service
        │                    │                              │
        ▼                    ▼                              ▼
 JWT Verification   Memory Intelligence         Conversation Management
                            │                              │
                            ▼                              ▼
                  Embedding Service              Context Retrieval
                            │                              │
                            ▼                              ▼
                 Query Rewrite Service         Chat Session Service
                            │                              │
                            ▼                              ▼
                Hybrid Retrieval Engine       Chat Message Service
                            │
                            ▼
                Cross Encoder Re-ranking
                            │
                            ▼
               Personalization Service
                            │
                            ▼
               Context Selector Service
                            │
                            ▼
                    Prompt Builder
                            │
                            ▼
                     Google Gemini
                            │
                            ▼
       Evaluation & Observability Services
                            │
                            ▼
                     SQLAlchemy ORM
                            │
      ┌─────────────────────┼──────────────────────┐
      ▼                     ▼                      ▼
 PostgreSQL + pgvector    Neo4j             Analytics Tables
```

---

# Backend Layered Architecture

```
Client

↓

API Routes

↓

Authentication

↓

Business Services

↓

AI Services

↓

Persistence Layer

↓

PostgreSQL + pgvector + Neo4j
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
- Query Rewrite Service
- Context Retrieval Service
- Cross Encoder Service
- Personalization Service
- Diversification Service
- Context Selector
- Prompt Builder
- LLM Service
- Chat Service
- Chat Session Service
- Chat Message Service
- Extraction Service
- Classification Service
- Ranking Service
- Tag Service
- Sentiment Service
- Temporal Service
- Graph Builder
- Neo4j Service
- Archive Service
- Forgetting Service
- Memory Cleanup Service
- Evaluation Service
- Observability Service
- Retrieval Analytics Service
- Usage Dashboard Service

---

## Database Layer

Technology

- PostgreSQL
- pgvector
- SQLAlchemy ORM
- Alembic
- Neo4j

Responsible for:

- User Data
- Memory Storage
- Vector Embeddings
- Hybrid Retrieval
- Knowledge Graph
- AI Analytics
- System Metrics
- Chat Sessions
- Chat Messages
- Conversation History

---

# Current Database Schema

```
users
│
├──────────────► memories
│                     │
│                     ▼
│             user_interactions
│
├──────────────► chat_sessions
│                     │
│                     ▼
│              chat_messages
│
└──────────────► ai_request_logs

system_metrics
```

---

# Request Flow (Memory Creation)

```
Client

↓

POST /memories

↓

Authentication

↓

Memory Service

↓

Entity Extraction

↓

Classification

↓

Importance Ranking

↓

Tag Generation

↓

Sentiment Analysis

↓

Embedding Generation

↓

Duplicate Detection

↓

Knowledge Graph Update

↓

Store Memory
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

Conversation Context

↓

Query Rewrite

↓

Semantic Search

+

Keyword Search

↓

Hybrid Retrieval

↓

Cross Encoder

↓

Personalization

↓

Context Selection

↓

Prompt Builder

↓

Gemini LLM

↓

Evaluation Logging

↓

Store Chat Messages

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
- Automatic Memory Extraction
- Memory Classification
- Importance Ranking
- Metadata Generation
- Sentiment Analysis
- Knowledge Graph Generation
- Duplicate Detection
- Long-Term Memory Management
- Semantic Search
- Hybrid Retrieval
- PostgreSQL Full Text Search
- Cross Encoder Re-ranking
- Personalized Retrieval
- Context-aware Retrieval
- Retrieval-Augmented Generation (RAG)
- AI Chat Endpoint
- AI Evaluation
- AI Observability
- Analytics Dashboards
- SQLAlchemy ORM
- Alembic Migrations
- Swagger Documentation
- Logging
- Persistent Chat Sessions
- Conversation History
- Multi-turn Conversations

---

# System Architecture Overview

```
                    React Frontend (Future)
                              │
                              ▼
                       FastAPI Backend
                              │
      ┌───────────────────────┼────────────────────────┐
      ▼                       ▼                        ▼
 Authentication         Memory Services         Chat Services
      │                       │                        │
      ▼                       ▼                        ▼
 PostgreSQL           AI Intelligence        Conversation Engine
      │                       │                        │
      ▼                       ▼                        ▼
 pgvector          Hybrid Retrieval         Prompt Builder
      │                       │                        │
      ▼                       ▼                        ▼
 Neo4j             Personalization         Google Gemini
                              │
                              ▼
                   Evaluation & Analytics
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
- Neo4j

## Artificial Intelligence

- Sentence Transformers
- all-MiniLM-L6-v2
- Cross Encoder (MS MARCO MiniLM)
- spaCy
- Google Gemini API
- Retrieval-Augmented Generation (RAG)

## Security

- JWT Authentication
- OAuth2PasswordBearer
- Password Hashing (bcrypt)

---

# Future Components

## Phase 8

- Document Intelligence
- OCR
- Chunking
- Document Embeddings
- Document Retrieval

## Phase 9

- Voice Intelligence
- Whisper Integration
- Voice Memories
- Image Understanding
- Multimodal Retrieval

## Phase 10

- Decision Engine
- Autonomous Planning
- Goal Tracking
- Recommendation Engine
- Agentic Workflows

---

# Deployment

## Development

- Windows 11
- Python
- FastAPI
- PostgreSQL
- pgvector
- Neo4j
- VS Code

## Production (Planned)

- React
- Docker
- AWS
- HTTPS
- PostgreSQL
- Neo4j
- Nginx
- CI/CD Pipeline

---

# Summary

With the completion of **Phase 7**, the AI Personal Memory & Decision Assistant has evolved into a production-grade intelligent memory platform.

The system now combines:

- Secure authentication
- Automatic memory understanding
- Knowledge graph construction
- Hybrid semantic and keyword retrieval
- Cross-encoder reranking
- Personalized memory retrieval
- Long-term memory management
- Retrieval-Augmented Generation (RAG)
- AI observability and analytics
- Performance monitoring
- Persistent conversations

The modular service-oriented architecture provides a scalable foundation for future expansion into document intelligence, multimodal AI, autonomous reasoning, and advanced decision-support capabilities.