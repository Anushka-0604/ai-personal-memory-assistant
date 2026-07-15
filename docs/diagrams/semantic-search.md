# System Architecture

**Project:** AI Personal Memory & Decision Assistant

**Architecture Version:** v0.4.0

**Last Updated:** After Phase 4

---

# Overview

The AI Personal Memory & Decision Assistant is designed as a modular, scalable, and production-oriented software system that combines modern backend engineering with Machine Learning.

The architecture follows a layered approach, where each component has a clearly defined responsibility. This separation of concerns improves maintainability, scalability, testing, and future extensibility.

At the end of Phase 4, the system consists of:

- Frontend Client
- FastAPI Backend
- Authentication Layer
- Business Logic Layer
- Machine Learning Layer
- PostgreSQL Database
- Vector Database (pgvector)
- Semantic Search Engine

Future phases will extend this architecture with Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), decision-making modules, and multi-modal memory support.

---

# High-Level Architecture

```text
                    +-----------------------+
                    |      Frontend         |
                    |  Web / Mobile Client  |
                    +-----------+-----------+
                                |
                           HTTPS / REST
                                |
                                ▼
                    +-----------------------+
                    |      FastAPI API      |
                    +-----------+-----------+
                                |
        +-----------------------+-----------------------+
        |                                               |
        ▼                                               ▼
+----------------------+                     +----------------------+
| Authentication Layer |                     | Business Logic Layer |
| JWT Authentication   |                     | Memory Services      |
+----------------------+                     +----------+-----------+
                                                        |
                                    +-------------------+-------------------+
                                    |                                       |
                                    ▼                                       ▼
                         +----------------------+               +----------------------+
                         | Embedding Service    |               | CRUD Operations      |
                         | SentenceTransformer  |               | Memory Management    |
                         +----------+-----------+               +----------------------+
                                    |
                                    ▼
                         +----------------------+
                         | Machine Learning     |
                         | all-MiniLM-L6-v2     |
                         +----------+-----------+
                                    |
                                    ▼
                         +----------------------+
                         | 384-D Embeddings     |
                         +----------+-----------+
                                    |
                                    ▼
                     +--------------------------------------+
                     | PostgreSQL 17 + pgvector             |
                     | Users                               |
                     | Memories                            |
                     | Embeddings                          |
                     +--------------------------------------+
```

---

# Layered Architecture

The system follows a layered architecture.

```
Presentation Layer

↓

API Layer

↓

Service Layer

↓

Machine Learning Layer

↓

Persistence Layer

↓

Database
```

Each layer has a single responsibility.

---

# 1. Presentation Layer

The presentation layer represents the client application.

Responsibilities

- User interaction
- Sending HTTP requests
- Displaying AI responses
- Authentication

Current implementation

- Swagger UI

Future implementation

- React Frontend
- Mobile Application

---

# 2. API Layer

Technology

- FastAPI

Responsibilities

- HTTP routing
- Request validation
- Response serialization
- Authentication
- Error handling

Current APIs

Authentication

```
POST /register

POST /login

GET /me
```

Memory APIs

```
POST /memories

GET /memories

GET /memories/{id}

PUT /memories/{id}

DELETE /memories/{id}

POST /memories/search
```

---

# 3. Authentication Layer

Authentication is implemented using JSON Web Tokens (JWT).

Workflow

```
User Login

↓

Verify Credentials

↓

Generate JWT

↓

Return Token

↓

Protected APIs
```

Responsibilities

- User verification
- Token generation
- Authorization
- Protected routes

---

# 4. Business Logic Layer

The service layer contains the application's core logic.

Current services

```
Memory Service

Embedding Service
```

Responsibilities

Memory Service

- Create memories
- Update memories
- Delete memories
- Search memories

Embedding Service

- Load ML model
- Generate embeddings
- Convert vectors

This layer remains independent from HTTP routing.

---

# 5. Machine Learning Layer

Introduced in Phase 4.

Purpose

Convert natural language into dense vector representations.

Model

```
Sentence Transformer

↓

all-MiniLM-L6-v2
```

Output

```
384-dimensional embeddings
```

Responsibilities

- Load pretrained model
- Generate embeddings
- Provide reusable embedding API

---

# 6. Persistence Layer

Technology

- SQLAlchemy ORM

Responsibilities

- ORM mapping
- Database communication
- Transactions
- Query abstraction

Current models

```
User

Memory
```

---

# 7. Database Layer

Technology

- PostgreSQL 17

Responsibilities

- Persistent storage
- ACID transactions
- User data
- Memory storage

Current tables

```
users

memories

alembic_version
```

---

# 8. Vector Database Layer

Technology

- pgvector

Purpose

Store vector embeddings directly inside PostgreSQL.

Current vector type

```
VECTOR(384)
```

Supported operations

- Cosine similarity
- Vector comparison
- Semantic retrieval

---

# Data Flow

## Memory Creation

```
User

↓

POST /memories

↓

FastAPI

↓

Memory Service

↓

Embedding Service

↓

Sentence Transformer

↓

Embedding

↓

PostgreSQL
```

---

## Memory Retrieval

```
GET /memories

↓

FastAPI

↓

Memory Service

↓

Database

↓

JSON Response
```

---

## Semantic Search

```
User Query

↓

Generate Query Embedding

↓

Cosine Similarity

↓

Top K Memories

↓

JSON Response
```

---

# Database Design

Current schema

```
Users

↓

1 : N

↓

Memories
```

Memory

```
id

user_id

content

embedding

source

created_at

updated_at
```

---

# Machine Learning Pipeline

```
Text

↓

Tokenizer

↓

Sentence Transformer

↓

Embedding

↓

Vector Database
```

---

# Semantic Search Pipeline

```
Question

↓

Embedding

↓

Vector Search

↓

Relevant Memories
```

This retrieval layer is the foundation for Retrieval-Augmented Generation.

---

# Design Principles

The project follows several software engineering principles.

## Separation of Concerns

Each module has a single responsibility.

Examples

Authentication

↓

Business Logic

↓

Machine Learning

↓

Database

---

## Modularity

Each service is independent.

Examples

```
embedding_service.py

memory_service.py
```

---

## Scalability

The architecture supports future additions without major redesign.

Upcoming modules

- LLM Service
- Prompt Builder
- Decision Engine
- Notification Engine

---

## Maintainability

Configuration values are stored in

```
.env
```

instead of being hardcoded.

Examples

- Database URL
- Secret Key
- Embedding Model

---

# Current Architecture (End of Phase 4)

```
Frontend

↓

FastAPI

↓

Authentication

↓

Business Logic

↓

Embedding Service

↓

Sentence Transformer

↓

PostgreSQL + pgvector

↓

Semantic Search
```

---

# Planned Architecture (Phase 5)

```
Frontend

↓

FastAPI

↓

Authentication

↓

Embedding Service

↓

Semantic Search

↓

Context Builder

↓

Prompt Builder

↓

Large Language Model

↓

AI Response
```

Phase 5 introduces Retrieval-Augmented Generation (RAG), enabling the system to generate intelligent responses grounded in the user's stored memories.

---

# Long-Term Vision

The final system will evolve into a production-ready AI assistant capable of:

- Long-term memory
- Semantic retrieval
- Personalized conversations
- Decision support
- Document understanding
- Multi-modal memory
- Real-time AI assistance
- Context-aware recommendations

---

# Summary

At the end of Phase 4, the AI Personal Memory & Decision Assistant has evolved from a conventional CRUD backend into a modular AI-powered system with semantic memory retrieval.

The architecture combines modern backend engineering practices with Machine Learning and vector databases, providing a scalable foundation for Retrieval-Augmented Generation and advanced conversational AI features in subsequent phases.