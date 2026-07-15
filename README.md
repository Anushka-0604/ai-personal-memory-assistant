# 🧠 AI Personal Memory & Decision Assistant

A production-level AI-powered **Personal Memory & Decision Assistant** that acts as a secure digital **"Second Brain"** for users.

The system enables users to securely store, organize, retrieve, and interact with their personal memories using **Machine Learning**, **Vector Databases**, **Semantic Search**, and, in future phases, **Large Language Models (LLMs)** and **Retrieval-Augmented Generation (RAG)**.

The project is being developed incrementally following production software engineering practices, with each phase introducing new architectural capabilities while maintaining modularity and scalability.

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
- AI Retrieval Layer (RAG Foundation)

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

## Machine Learning

- Sentence Transformers
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

- OpenAI API / Gemini API
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
│   ├── .env
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

---

## Memory Engine

- Memory CRUD
- User-specific Storage
- Service Layer Architecture

---

## Artificial Intelligence

- Sentence Embeddings
- Automatic Embedding Generation
- Vector Database Integration
- Semantic Search
- Cosine Similarity Search
- Meaning-based Memory Retrieval

---

# 🏗 Current System Architecture

```text
Frontend

↓

FastAPI Backend

↓

Authentication

↓

Business Logic

↓

Embedding Service

↓

Sentence Transformer

↓

384-Dimensional Embeddings

↓

PostgreSQL + pgvector

↓

Semantic Search
```

---

# 📈 Development Roadmap

| Phase | Status |
|--------|--------|
| Phase 1 – Project Setup | ✅ Completed |
| Phase 2 – Backend Foundation & Authentication | ✅ Completed |
| Phase 3 – Memory Engine | ✅ Completed |
| Phase 4 – AI Memory Engine & Semantic Search | ✅ Completed |
| Phase 5 – LLM Integration & Retrieval-Augmented Generation | 🔄 Next |
| Phase 6 – Long-Term Memory & Context Management | ⏳ Planned |
| Phase 7 – Decision Intelligence Engine | ⏳ Planned |
| Phase 8 – Production Deployment & Scaling | ⏳ Planned |

---

# 🎯 Upcoming Features (Phase 5)

- OpenAI / Gemini Integration
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- Conversational AI
- Context Builder
- Personalized AI Responses
- AI Chat Endpoint
- Intelligent Memory Retrieval

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
- Semantic Search Pipeline
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
- Production Architecture
- Cloud-ready Development

The long-term vision is to build an intelligent personal assistant capable of understanding, remembering, and reasoning over a user's personal knowledge in a secure and scalable manner.

---

# 📄 License

This project is being developed for educational purposes, portfolio development, and practical learning in Software Engineering, Artificial Intelligence, Machine Learning, Full Stack Development, and Distributed Systems.