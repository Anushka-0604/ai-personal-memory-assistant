# 🧠 AI Personal Memory & Decision Assistant

A production-level AI-powered **Personal Memory & Decision Assistant** that acts as a secure digital **"Second Brain"** for users.

The system enables users to securely store, organize, retrieve, and interact with their personal memories using **Machine Learning**, **Vector Databases**, **Semantic Search**, and **Retrieval-Augmented Generation (RAG)** powered by **Google Gemini**.

The project is being developed incrementally following production software engineering practices, with each phase introducing new architectural capabilities while maintaining modularity, scalability, and clean software design.

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
- Alembic Vector Migration

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
- Retrieval Foundation

---

## ✅ Phase 5 – Retrieval-Augmented Generation (RAG)

**Status:** Completed

### Large Language Model

- Google Gemini Integration
- Gemini API
- LLM Service
- Prompt Engineering

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
- AI Question Answering
- Personalized Responses

### Reliability

- Logging
- Graceful Gemini Error Handling
- Modular AI Services

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

---

## Artificial Intelligence

- Sentence Transformers
- all-MiniLM-L6-v2
- Google Gemini API
- Retrieval-Augmented Generation (RAG)

---

## Machine Learning

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

---

# 📂 Project Structure

```text
AI-Personal-Memory-Assistant/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
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
| POST | `/memories/search` | Semantic Memory Search |

---

## AI APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/chat` | AI Chat using Retrieval-Augmented Generation |

---

# ✨ Current Features

## Authentication

- User Registration
- User Login
- JWT Authorization
- Secure Password Hashing

---

## Database

- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations
- Relational Data Modeling
- pgvector Integration

---

## Memory Engine

- Memory CRUD
- User-specific Storage
- Automatic Embedding Generation
- Automatic Embedding Updates

---

## Artificial Intelligence

- Sentence Embeddings
- Semantic Search
- Cosine Similarity Search
- Vector Database
- Retrieval-Augmented Generation (RAG)
- Prompt Builder
- Google Gemini Integration
- AI Chat
- Memory-Grounded Responses

---

# 🏗 Current System Architecture

```text
User

↓

FastAPI Backend

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

Google Gemini

↓

AI Response
```

---

# 📈 Development Roadmap

| Phase | Status |
|--------|--------|
| Phase 1 – Project Setup | ✅ Completed |
| Phase 2 – Backend Foundation & Authentication | ✅ Completed |
| Phase 3 – Memory Engine | ✅ Completed |
| Phase 4 – AI Memory Engine & Semantic Search | ✅ Completed |
| Phase 5 – Retrieval-Augmented Generation (RAG) | ✅ Completed |
| Phase 6 – Conversational Memory & Automatic Memory Extraction | 🚀 Next |
| Phase 7 – Context Management & Memory Optimization | ⏳ Planned |
| Phase 8 – Decision Intelligence Engine | ⏳ Planned |
| Phase 9 – Production Deployment & Multi-modal AI | ⏳ Planned |

---

# 🎯 Upcoming Features (Phase 6)

- Conversation History
- Automatic Memory Extraction
- Session-Based Conversations
- Short-Term Conversational Memory
- Combined Short-Term and Long-Term Memory
- Multi-turn AI Conversations
- Automatic Memory Saving
- Improved Context Management

---

# 📚 Documentation

Comprehensive technical documentation is available inside the **`docs/`** directory.

Documentation includes:

- Phase-wise Development
- System Architecture
- AI Architecture
- API Documentation
- Database Documentation
- Vector Database Design
- RAG Pipeline
- System Diagrams

---

# 🎓 Project Goal

This project is being developed as a **production-quality AI SaaS application** to demonstrate:

- Software Engineering
- Backend Development
- System Design
- Artificial Intelligence
- Machine Learning
- Vector Databases
- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Production Architecture
- Cloud-ready Development

The long-term vision is to build an intelligent personal assistant capable of understanding, remembering, reasoning, and making context-aware decisions using a combination of long-term semantic memory, conversational memory, and modern AI technologies.

---

# 📄 License

This project is being developed for educational purposes, portfolio development, and practical learning in Software Engineering, Artificial Intelligence, Machine Learning, Full Stack Development, and Distributed Systems.