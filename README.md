# 🧠 AI Personal Memory & Decision Assistant

A production-level AI-powered **Personal Memory & Decision Assistant** that acts as a secure digital **"Second Brain"** for users.

The system enables users to securely store, organize, retrieve, and interact with their personal memories using **Machine Learning**, **Vector Databases**, **Knowledge Graphs**, **Hybrid Retrieval**, **Semantic Search**, **Personalized Retrieval**, **Retrieval-Augmented Generation (RAG)**, and **Conversational AI** powered by **Google Gemini**.

The project is being developed incrementally following production software engineering practices, with each phase introducing new architectural capabilities while maintaining modularity, scalability, security, and clean software design.

---

# 🚀 Current Project Status

## ✅ Phase 1 – Project Setup

**Status:** Completed

### Features

- Development Environment Setup
- Python Virtual Environment
- FastAPI Installation
- Professional Project Structure
- Git Initialization
- GitHub Repository Setup
- Configuration Management
- Environment Variables
- Documentation Framework

---

## ✅ Phase 2 – Backend Foundation & Authentication

**Status:** Completed

### Backend

- FastAPI Backend
- Layered Architecture
- Dependency Injection
- Configuration Management

### Database

- PostgreSQL Integration
- SQLAlchemy ORM
- Alembic Database Migrations

### Authentication

- User Registration
- User Login
- Password Hashing (bcrypt)
- JWT Authentication
- OAuth2PasswordBearer
- Protected Routes

### API Endpoints

- POST `/register`
- POST `/login`
- GET `/me`

---

## ✅ Phase 3 – Memory Engine

**Status:** Completed

### Database

- Memory Model
- User–Memory Relationship
- Alembic Migration
- Memory Persistence

### CRUD Operations

- Create Memory
- Retrieve Memory
- Update Memory
- Delete Memory

### API Endpoints

- POST `/memories`
- GET `/memories`
- GET `/memories/{id}`
- PUT `/memories/{id}`
- DELETE `/memories/{id}`

### Security

- JWT Protected Memory APIs
- User-specific Memory Access
- Authorization Checks

---

## ✅ Phase 4 – AI Memory Engine & Semantic Search

**Status:** Completed

### Machine Learning

- Sentence Transformers Integration
- all-MiniLM-L6-v2 Embedding Model
- Automatic Embedding Generation
- Automatic Embedding Updates

### Vector Database

- PostgreSQL 17
- pgvector Extension
- VECTOR(384) Storage

### AI Services

- Embedding Service
- Semantic Search Service
- Cosine Similarity Search
- Top-K Memory Retrieval

### APIs

- POST `/memories/search`
- AI-Enhanced Memory Creation
- Automatic Embedding Pipeline

### AI Capabilities

- Semantic Memory Retrieval
- Meaning-based Search
- Vector Similarity Search
- Long-Term Memory Foundation

---

## ✅ Phase 5 – Retrieval-Augmented Generation (RAG)

**Status:** Completed

### Large Language Model

- Google Gemini Integration
- Gemini API
- LLM Service
- Prompt Builder

### Retrieval-Augmented Generation

- Query Embedding Generation
- Semantic Vector Search
- Top-K Memory Retrieval
- Similarity Threshold Filtering
- Prompt Builder
- Context Construction
- Memory-Grounded Responses

### AI Chat

- Protected Chat Endpoint
- Chat Service
- Personalized Responses

### Reliability

- Logging
- Graceful Gemini Error Handling
- Modular AI Services

---

## ✅ Phase 6 – Conversational Memory & Chat Management

**Status:** Completed

### Conversation Management

- Persistent Chat Sessions
- Conversation History
- Multi-turn Conversations
- Session-based Chat Management
- Short-Term Conversational Memory

### Database

- Chat Sessions Table
- Chat Messages Table
- Persistent Conversation Storage

### AI Enhancements

- Conversation-Aware RAG
- Combined Long-Term and Short-Term Memory
- Context-Aware Prompt Construction
- Conversation History Retrieval
- Enhanced Prompt Builder

### Services

- Chat Session Service
- Chat Message Service
- Updated Chat Service
- Updated Prompt Builder

### APIs

- Chat Session APIs
- Conversation History APIs
- Updated AI Chat Endpoint

---

## ✅ Phase 7 – Advanced Memory Intelligence

**Status:** Completed

### Module 1 – Automatic Memory Extraction

- Entity Extraction using spaCy
- Gemini-based Information Extraction
- Temporal Information Extraction
- Automatic Structured Metadata Extraction
- Knowledge Graph Generation
- Neo4j Integration

### Module 2 – Memory Classification

- Automatic Memory Classification
- Category Detection
- Classification Service

### Module 3 – Importance Ranking

- Importance Scoring
- Recency Scoring
- Weighted Memory Ranking

### Module 4 – Memory Metadata

- Automatic Tag Generation
- Sentiment Analysis
- Confidence Scores
- Metadata Enrichment
- Temporal Metadata Storage

### Module 5 – Intelligent Context Selection

- Multi-factor Ranking
- Category-aware Ranking
- Intelligent Context Selection
- Context Selector Service

### Module 6 – Conversation Intelligence

- Reference Resolution
- Conversation Context Management
- Context-aware Retrieval
- Conversation Memory Integration

### Module 7 – Long-Term Memory Management

- Duplicate Detection
- Evidence Tracking
- Memory Reinforcement
- Memory Decay
- Automatic Archive Strategy
- Forgetting Strategy
- Memory Cleanup Service

### Module 8 – Advanced Memory Retrieval

- Query Rewrite
- Hybrid Retrieval
- PostgreSQL Full-Text Search
- Metadata Filtering
- Cross Encoder Re-ranking
- Retrieval Diversification

### Module 9 – Personalized Memory Retrieval

- Personalization Service
- User Interaction Scoring
- Personalized Ranking
- Context-aware Retrieval
- Adaptive Retrieval Pipeline

### Module 10 – AI Observability & Evaluation

- AI Request Logging
- Retrieval Analytics
- Usage Dashboard
- AI Dashboard
- Evaluation Service
- Observability Service
- System Metrics
- Performance Monitoring

---

# 🛠 Technology Stack

## Frontend *(Planned)*

- React
- TypeScript
- Tailwind CSS

---

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic

---

## Database

- PostgreSQL 17
- pgvector
- Neo4j

---

## Artificial Intelligence

- Google Gemini API
- Retrieval-Augmented Generation (RAG)
- Hybrid Retrieval
- Personalized Retrieval
- Knowledge Graph
- Prompt Engineering
- Semantic Search
- AI Observability
- Retrieval Analytics

---

## Machine Learning

- Sentence Transformers
- all-MiniLM-L6-v2
- Cross Encoder (MS MARCO MiniLM)
- spaCy
- PyTorch
- Transformers
- NumPy
- pgvector (Python)

---

## Authentication

- JWT
- OAuth2PasswordBearer
- Passlib (bcrypt)
- Python-JOSE

---

## Future AI Stack

- LangChain
- LlamaIndex
- Whisper
- WebRTC
- MinIO
- Redis
- Celery

# 📂 Project Structure

```text
AI-Personal-Memory-Assistant/

├── backend/
│   ├── app/
│   │
│   ├── api/
│   │
│   ├── core/
│   │
│   ├── database/
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │   │
│   │   ├── authentication_service.py
│   │   ├── memory_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── prompt_builder.py
│   │   ├── chat_service.py
│   │   ├── chat_session_service.py
│   │   ├── chat_message_service.py
│   │   │
│   │   ├── extraction_service.py
│   │   ├── entity_extractor.py
│   │   ├── gemini_extractor.py
│   │   ├── temporal_service.py
│   │   ├── classification_service.py
│   │   ├── ranking_service.py
│   │   ├── tag_service.py
│   │   ├── sentiment_service.py
│   │   ├── graph_builder.py
│   │   ├── neo4j_service.py
│   │   ├── context_selector.py
│   │   ├── query_rewrite_service.py
│   │   ├── cross_encoder_service.py
│   │   ├── diversification_service.py
│   │   ├── personalization_service.py
│   │   ├── context_retrieval_service.py
│   │   ├── archive_service.py
│   │   ├── forgetting_service.py
│   │   ├── memory_cleanup_service.py
│   │   ├── evaluation_service.py
│   │   ├── observability_service.py
│   │   ├── retrieval_analytics_service.py
│   │   ├── retrieval_quality_service.py
│   │   ├── usage_dashboard_service.py
│   │   ├── ai_dashboard_service.py
│   │   ├── cache_service.py
│   │   └── system_metric_service.py
│   │
│   ├── utils/
│   └── main.py
│
├── alembic/
│
├── tests/
│
├── frontend/
│
├── docs/
│   ├── api/
│   ├── architecture/
│   ├── database/
│   ├── diagrams/
│   ├── phases/
│   └── README.md
│
└── README.md
```

---

# 🔗 Current API Endpoints

## Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate user |
| GET | `/me` | Retrieve current user |

---

## Memory APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/memories` | Create Memory |
| GET | `/memories` | Retrieve All Memories |
| GET | `/memories/{id}` | Retrieve Memory by ID |
| PUT | `/memories/{id}` | Update Memory |
| DELETE | `/memories/{id}` | Delete Memory |
| POST | `/memories/search` | Hybrid Memory Search |

---

## Chat APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/chat` | Generate AI response |
| POST | `/chat/sessions` | Create chat session |
| GET | `/chat/sessions` | Retrieve chat sessions |
| GET | `/chat/sessions/{session_id}` | Retrieve chat session |
| PUT | `/chat/sessions/{session_id}` | Rename chat session |
| DELETE | `/chat/sessions/{session_id}` | Delete chat session |
| GET | `/chat/sessions/{session_id}/messages` | Retrieve conversation history |

---

## Analytics APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/analytics/retrieval-quality` | Retrieval quality metrics |
| GET | `/analytics/usage-dashboard` | AI usage statistics |
| GET | `/analytics/ai-dashboard` | Unified AI dashboard |

---

# ✨ Current Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Secure Password Hashing
- Protected API Endpoints

---

## Database

- PostgreSQL 17
- pgvector Integration
- Neo4j Knowledge Graph
- SQLAlchemy ORM
- Alembic Migrations
- Persistent Chat Sessions
- Persistent Conversation History
- AI Request Logs
- System Metrics

---

## Memory Engine

- Memory CRUD Operations
- User-specific Memory Storage
- Automatic Entity Extraction
- Automatic Memory Classification
- Automatic Metadata Generation
- Sentiment Analysis
- Automatic Tag Generation
- Importance Ranking
- Duplicate Detection
- Evidence Tracking
- Long-Term Memory Management
- Archive Strategy
- Forgetting Strategy

---

## AI & Retrieval

- Sentence Embeddings
- Semantic Search
- PostgreSQL Full-Text Search
- Hybrid Retrieval
- Query Rewriting
- Cross Encoder Re-ranking
- Personalized Retrieval
- Context-aware Retrieval
- Metadata Filtering
- Intelligent Context Selection
- Knowledge Graph Generation
- Retrieval-Augmented Generation (RAG)
- Conversation-aware RAG
- Google Gemini Integration
- Memory-grounded Responses
- Context-aware Responses

---

## Monitoring & Analytics

- AI Request Logging
- Retrieval Analytics
- Retrieval Quality Evaluation
- Usage Dashboard
- AI Dashboard
- System Metrics
- Performance Monitoring
- Observability
- Embedding Cache

---

# 🏗 Current System Architecture

```text
                          User
                            │
                            ▼
                     FastAPI Backend
                            │
      ┌─────────────────────┼──────────────────────────────┐
      ▼                     ▼                              ▼
Authentication        Memory Service                 Chat Service
      │                     │                              │
      ▼                     ▼                              ▼
JWT Verification  Memory Intelligence          Conversation Management
                          │                              │
                          ▼                              ▼
                Embedding Service            Context Retrieval
                          │                              │
                          ▼                              ▼
               Query Rewrite Service        Chat Session Service
                          │                              │
                          ▼                              ▼
              Hybrid Retrieval Engine      Chat Message Service
                          │
                          ▼
              Cross Encoder Re-ranking
                          │
                          ▼
             Personalization Service
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
      Evaluation & Observability Services
                          │
                          ▼
                    SQLAlchemy ORM
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
 PostgreSQL + pgvector   Neo4j       Analytics Tables
```

# 📈 Development Roadmap

| Phase | Status |
|--------|--------|
| Phase 1 – Project Setup | ✅ Completed |
| Phase 2 – Backend Foundation & Authentication | ✅ Completed |
| Phase 3 – Memory Engine | ✅ Completed |
| Phase 4 – AI Memory Engine & Semantic Search | ✅ Completed |
| Phase 5 – Retrieval-Augmented Generation (RAG) | ✅ Completed |
| Phase 6 – Conversational Memory & Chat Management | ✅ Completed |
| Phase 7 – Advanced Memory Intelligence | ✅ Completed |
| Phase 8 – Document Intelligence | ⏳ Planned |
| Phase 9 – Multimodal AI | ⏳ Planned |
| Phase 10 – Decision Intelligence Engine | ⏳ Planned |

---

# 🎯 Upcoming Features (Phase 8)

The next phase focuses on enabling the assistant to understand, process, and retrieve information from uploaded documents.

### Planned Features

- Document Upload
- OCR Integration
- PDF Processing
- DOCX Processing
- Intelligent Text Extraction
- Automatic Chunking
- Document Embeddings
- Hybrid Document Retrieval
- Document-Augmented Generation (DocRAG)
- Document Metadata Extraction
- Document Classification
- Document Search
- Multi-document Retrieval

---

# 📚 Documentation

Comprehensive technical documentation is available inside the **`docs/`** directory.

Documentation includes:

- Phase-wise Development
- System Architecture
- AI Architecture
- API Documentation
- Database Documentation
- Alembic Migration History
- Vector Database Design
- Hybrid Retrieval Architecture
- Knowledge Graph Architecture
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Conversational RAG
- AI Observability
- AI Analytics
- System Diagrams

---

# 🎓 Project Goal

This project is being developed as a **production-quality AI SaaS application** that serves as a secure digital **Second Brain** for users.

It demonstrates practical implementation of:

- Software Engineering
- Backend Development
- System Design
- Artificial Intelligence
- Machine Learning
- Vector Databases
- Knowledge Graphs
- Semantic Search
- Hybrid Retrieval
- Personalized Retrieval
- Retrieval-Augmented Generation (RAG)
- Conversational AI
- Large Language Models (LLMs)
- AI Observability
- Production Architecture
- Cloud-ready Development

With the completion of **Phase 7**, the assistant is capable of:

- Understanding user memories automatically
- Extracting entities and structured metadata
- Building a Knowledge Graph
- Managing long-term memory intelligently
- Detecting duplicate memories
- Reinforcing important memories
- Archiving and forgetting inactive memories
- Performing hybrid semantic and keyword retrieval
- Re-ranking memories using AI
- Personalizing retrieval using user interactions
- Maintaining multi-turn conversational context
- Monitoring AI performance through analytics and observability
- Generating personalized, memory-grounded AI responses

Future phases will extend the assistant with document intelligence, multimodal AI, autonomous reasoning, intelligent planning, and decision-support capabilities.

---

# 🌟 Key Highlights

The project currently includes:

- ✅ Production-ready FastAPI backend
- ✅ JWT Authentication
- ✅ PostgreSQL + pgvector
- ✅ Neo4j Knowledge Graph
- ✅ Semantic Search
- ✅ Hybrid Retrieval
- ✅ Cross-Encoder Re-ranking
- ✅ Personalized Retrieval
- ✅ Automatic Memory Extraction
- ✅ Knowledge Graph Construction
- ✅ Long-Term Memory Management
- ✅ Conversational Retrieval-Augmented Generation (RAG)
- ✅ Google Gemini Integration
- ✅ AI Analytics & Observability
- ✅ Modular Service-Oriented Architecture

---

# 📄 License

This project is being developed for educational purposes, portfolio development, research, and practical learning in:

- Software Engineering
- Artificial Intelligence
- Machine Learning
- Backend Development
- System Design
- Knowledge Graphs
- Vector Databases
- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Conversational AI
- Production AI Systems
- Cloud-native Application Development

---

# 🙌 Acknowledgements

This project builds upon several open-source technologies and frameworks, including:

- FastAPI
- PostgreSQL
- pgvector
- SQLAlchemy
- Alembic
- Sentence Transformers
- PyTorch
- spaCy
- Neo4j
- Google Gemini API

These technologies provide the foundation for building a scalable, production-grade AI Personal Memory & Decision Assistant.