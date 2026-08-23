# System Architecture

## Overview

The AI Personal Memory & Decision Assistant is a production-level AI application designed to act as a secure digital second brain.

The system follows a layered architecture to ensure scalability, maintainability, modularity, and clean separation of concerns.

With the completion of **Phase 8**, the system has evolved from an intelligent memory platform into a **document-aware AI intelligence platform** supporting automatic memory understanding, document intelligence, semantic document retrieval, hybrid memory + document RAG, knowledge graph integration, cross-document relationships, personalized retrieval, AI observability, analytics, performance monitoring, and system health monitoring.

---

# Current Architecture (Phase 8)

```text
                              User
                                │
                                ▼
                         FastAPI Backend
                                │
       ┌────────────────────────┼─────────────────────────────┐
       ▼                        ▼                             ▼
 Authentication          Memory Services                Document Services
       │                        │                             │
       ▼                        ▼                             ▼
 JWT Verification       Memory Intelligence          Document Ingestion
                                │                             │
                                ▼                             ▼
                       Embedding Service              Text Extraction
                                │                             │
                                ▼                             ▼
                       Hybrid Retrieval              Document Intelligence
                                │                    ┌────────┼─────────┐
                                │                    ▼        ▼         ▼
                                │              Classification Keywords  NER
                                │                              │
                                │                              ▼
                                │                     Relationship Extraction
                                │                              │
                                │                              ▼
                                │                       Document Chunking
                                │                              │
                                │                              ▼
                                │                       Document Embeddings
                                │                              │
                                └──────────────┬───────────────┘
                                               ▼
                                  Unified Retrieval Layer
                                               │
                                               ▼
                                   Cross Encoder Re-ranking
                                               │
                                               ▼
                                     Personalization Service
                                               │
                                               ▼
                                    Diversification Service
                                               │
                                               ▼
                                  Intelligent Context Selector
                                               │
                                               ▼
                                          Prompt Builder
                                               │
                                               ▼
                                         Google Gemini
                                               │
                                               ▼
                                  Evaluation & Analytics
                                               │
                     ┌─────────────────────────┼──────────────────────┐
                     ▼                         ▼                      ▼
               Performance                System Health         AI Dashboard
               Monitoring                 Monitoring             Analytics
                                               │
                                               ▼
                                        Persistence Layer
                                               │
                    ┌──────────────────────────┼──────────────────────┐
                    ▼                          ▼                      ▼
             PostgreSQL + pgvector          Neo4j              Analytics Tables
```

---

# Backend Layered Architecture

```text
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

Document Intelligence

↓

Knowledge Graph Services

↓

Persistence Layer

↓

PostgreSQL + pgvector + Neo4j
```

---

# Backend Components

## API Layer

Responsible for:

* HTTP Endpoints
* Request Validation
* Response Models
* Dependency Injection
* JWT-Protected APIs
* Document APIs
* Chat APIs
* Graph Query APIs
* Analytics APIs
* Health APIs

---

## Authentication Layer

Responsible for:

* User Registration
* User Login
* JWT Authentication
* OAuth2PasswordBearer
* Protected Endpoints
* User resource ownership validation

---

# Service Layer

Responsible for application business logic and AI processing.

### Core Services

* Authentication Service
* Memory Service
* Document Service
* Embedding Service
* Chat Service
* Chat Session Service
* Chat Message Service

### Memory Intelligence

* Extraction Service
* Classification Service
* Ranking Service
* Tag Service
* Sentiment Service
* Temporal Service
* Archive Service
* Forgetting Service
* Memory Cleanup Service

### Retrieval and AI

* Query Rewrite Service
* Context Retrieval Service
* Cross Encoder Service
* Personalization Service
* Diversification Service
* Context Selector
* Prompt Builder
* LLM Service

### Document Intelligence

* Document Extraction Service
* Document Chunking Service
* Document Search Service
* Classification Service
* Keyword Extraction Service
* NER Service
* Relationship Extraction Service

### Knowledge Graph

* Graph Builder
* Neo4j Service
* Graph Query Service

### Memory-Document Integration

* Memory Document Service

### Analytics and Monitoring

* Evaluation Service
* Retrieval Analytics Service
* Retrieval Quality Service
* Usage Dashboard Service
* Document Dashboard Service
* System Metric Service
* Health Service
* AI Dashboard Service

---

# Database Layer

Technology:

* PostgreSQL
* pgvector
* SQLAlchemy ORM
* Alembic
* Neo4j

Responsible for:

* User Data
* Memory Storage
* Vector Embeddings
* Document Storage
* Document Chunks
* Semantic Retrieval
* Hybrid Retrieval
* Knowledge Graph
* Memory-Document Relationships
* Chat Sessions
* Chat Messages
* Conversation History
* AI Request Logs
* Retrieval Logs
* System Metrics
* Analytics Data

---

# Current Database Architecture

```text
users
│
├──────────────► memories
│                    │
│                    ▼
│             user_interactions
│
├──────────────► chat_sessions
│                    │
│                    ▼
│              chat_messages
│
├──────────────► documents
│                    │
│                    ▼
│              document_chunks
│
├──────────────► ai_request_logs
│
└──────────────► retrieval_logs

system_metrics
```

Memory and document relationships are additionally maintained through the memory-document integration layer.

Knowledge graph information is maintained in Neo4j:

```text
Document
   │
   ▼
Entity
   │
   ▼
Relationship
   │
   ▼
Cross-Document Connections
```

---

# Request Flow — Memory Creation

```text
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

# Request Flow — Document Creation

```text
Client

↓

POST /documents/upload

↓

Authentication

↓

Document Service

↓

File Storage

↓

Text Extraction

↓

Document Classification

↓

Keyword Extraction

↓

Named Entity Recognition

↓

Relationship Extraction

↓

Document Chunking

↓

Embedding Generation

↓

PostgreSQL + pgvector

↓

Neo4j Knowledge Graph
```

---

# Request Flow — AI Chat

```text
Client

↓

POST /chat

↓

Authentication

↓

Conversation Context

↓

Reference Resolution

↓

Query Rewrite

↓

Memory Retrieval
+
Document Retrieval

↓

Unified Retrieval

↓

Cross Encoder

↓

Personalization

↓

Diversification

↓

Context Selection

↓

Prompt Builder

↓

Gemini LLM

↓

Evaluation Logging

↓

Performance Logging

↓

Store Chat Messages

↓

AI Response
```

---

# Request Flow — Graph Retrieval

```text
Client

↓

Graph Query API

↓

Graph Query Service

↓

Neo4j

↓

Entity / Relationship Traversal

↓

Cross-Document Relationships

↓

Graph Retrieval

↓

API Response
```

---

# Current Features

Implemented:

* JWT Authentication
* OAuth2 Authorization
* User Registration
* User Login
* Memory CRUD APIs
* Automatic Memory Extraction
* Memory Classification
* Importance Ranking
* Metadata Generation
* Sentiment Analysis
* Knowledge Graph Generation
* Duplicate Detection
* Long-Term Memory Management
* Semantic Search
* Hybrid Retrieval
* PostgreSQL Full Text Search
* Cross Encoder Re-ranking
* Personalized Retrieval
* Context-Aware Retrieval
* Retrieval-Augmented Generation (RAG)
* AI Chat Endpoint
* AI Evaluation
* AI Observability
* Analytics Dashboards
* SQLAlchemy ORM
* Alembic Migrations
* Swagger Documentation
* Logging
* Persistent Chat Sessions
* Conversation History
* Multi-turn Conversations
* Document Upload
* Document Text Extraction
* Document Classification
* Keyword Extraction
* Named Entity Recognition
* Relationship Extraction
* Document Chunking
* Document Embeddings
* Semantic Document Search
* Document-Aware RAG
* Memory + Document Unified Retrieval
* Memory ↔ Document Integration
* Neo4j Document Knowledge Graph
* Cross-Document Relationships
* Graph Query APIs
* Multi-Hop Graph Retrieval
* Document Analytics
* Retrieval Analytics
* Usage Analytics
* Performance Monitoring
* System Health Monitoring
* AI Dashboard

---

# System Architecture Overview

```text
                    React Frontend (Future)
                              │
                              ▼
                       FastAPI Backend
                              │
       ┌──────────────────────┼─────────────────────────┐
       ▼                      ▼                         ▼
 Authentication        Memory Services           Document Services
       │                      │                         │
       ▼                      ▼                         ▼
 PostgreSQL            AI Intelligence          Document Intelligence
       │                      │                         │
       ▼                      ▼                         ▼
    pgvector            Hybrid Retrieval       Document Embeddings
       │                      │                         │
       │                      ▼                         │
       │               Personalization                 │
       │                      │                         │
       │                      ▼                         │
       │               Context Selection               │
       │                      │                         │
       └───────────────┬──────┴─────────────────────────┘
                       ▼
                 Unified RAG Context
                       │
                       ▼
                 Prompt Builder
                       │
                       ▼
                 Google Gemini
                       │
                       ▼
             Evaluation & Analytics
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
        Retrieval   Performance  Health
        Analytics   Monitoring   Monitoring

                    Neo4j
                      │
                      ▼
             Knowledge Graph
                      │
                      ▼
        Entity & Relationship Retrieval
```

---

# Current Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic

## Database

* PostgreSQL
* pgvector
* Neo4j

## Artificial Intelligence

* Sentence Transformers
* all-MiniLM-L6-v2
* Cross Encoder (MS MARCO MiniLM)
* spaCy
* Google Gemini API
* Retrieval-Augmented Generation (RAG)
* Document Intelligence Services

## Document Intelligence

* Document Text Extraction
* Document Chunking
* Document Embeddings
* Semantic Document Search
* Named Entity Recognition
* Keyword Extraction
* Relationship Extraction
* Document Classification

## Security

* JWT Authentication
* OAuth2PasswordBearer
* Password Hashing (bcrypt)

## Monitoring and Analytics

* AI Request Logging
* Retrieval Analytics
* Usage Analytics
* System Metrics
* Health Monitoring
* AI Dashboard

---

# Future Components

## Phase 9

Expand beyond text with multimodal AI:

* Voice Intelligence
* Whisper Integration
* Voice Memories
* Image Understanding
* Image Embeddings
* Multimodal Retrieval
* Cross-Modal Retrieval

## Phase 10

Introduce intelligent reasoning capabilities:

* Decision Engine
* Autonomous Planning
* Goal Tracking
* Recommendation Engine
* Preference Learning
* Agentic Workflows
* Advanced Knowledge Graph Reasoning

---

# Deployment

## Development

* Windows 11
* Python
* FastAPI
* PostgreSQL
* pgvector
* Neo4j
* VS Code

## Production (Planned)

* React
* Docker
* AWS
* HTTPS
* PostgreSQL
* Neo4j
* Nginx
* CI/CD Pipeline

---

# Summary

With the completion of **Phase 8**, the AI Personal Memory & Decision Assistant has evolved into a production-grade **memory and document intelligence platform**.

The system now combines:

* Secure authentication
* Automatic memory understanding
* Knowledge graph construction
* Hybrid semantic and keyword retrieval
* Cross-encoder reranking
* Personalized memory retrieval
* Long-term memory management
* Document ingestion
* Document intelligence
* Document chunking and embeddings
* Semantic document retrieval
* Document-aware RAG
* Unified memory + document retrieval
* Memory ↔ Document integration
* Cross-document knowledge retrieval
* Multi-hop graph retrieval
* Retrieval analytics
* Usage analytics
* AI observability
* Performance monitoring
* System health monitoring
* AI dashboards
* Persistent conversations

The modular, service-oriented architecture provides a scalable foundation for future expansion into **multimodal AI, voice and image intelligence, autonomous reasoning, agentic workflows, and advanced decision-support capabilities**.

**PHASE 8 — DOCUMENT INTELLIGENCE: 100% COMPLETE ✅**
