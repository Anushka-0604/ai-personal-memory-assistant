# 🧠 AI Personal Memory & Decision Assistant

A production-level AI-powered **Personal Memory & Decision Assistant** that acts as a secure digital **"Second Brain"** for users.

The system enables users to securely store, organize, retrieve, and interact with their personal memories using **Machine Learning**, **Vector Databases**, **Semantic Search**, **Retrieval-Augmented Generation (RAG)**, and **Conversational AI** powered by **Google Gemini**.

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
- Conversational RAG
- Prompt Engineering
- Semantic Search

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
│   │   │   ├── embedding_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── memory_service.py
│   │   │   ├── prompt_builder.py
│   │   │   ├── chat_service.py
│   │   │   ├── chat_session_service.py
│   │   │   └── chat_message_service.py
│   │   │
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

## Chat APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/chat` | Generate an AI response using Conversational RAG |
| POST | `/chat/sessions` | Create a new chat session |
| GET | `/chat/sessions` | Retrieve all chat sessions |
| GET | `/chat/sessions/{session_id}` | Retrieve a specific chat session |
| PUT | `/chat/sessions/{session_id}` | Rename a chat session |
| DELETE | `/chat/sessions/{session_id}` | Delete a chat session |
| GET | `/chat/sessions/{session_id}/messages` | Retrieve conversation history |

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
- SQLAlchemy ORM
- Alembic Migrations
- Relational Data Modeling
- pgvector Integration
- Persistent Chat Sessions
- Persistent Conversation History

---

## Memory Engine

- Memory CRUD Operations
- User-specific Memory Storage
- Automatic Embedding Generation
- Automatic Embedding Updates
- Semantic Memory Retrieval

---

## Conversational AI

- Sentence Embeddings
- Semantic Search
- Cosine Similarity Search
- Vector Database
- Retrieval-Augmented Generation (RAG)
- Conversational RAG
- Prompt Builder
- Google Gemini Integration
- Persistent Chat Sessions
- Conversation History
- Multi-turn Conversations
- Context-Aware Responses
- Memory-Grounded Responses

---

# 🏗 Current System Architecture

```text
                     User
                       │
                       ▼
                 FastAPI Backend
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
Authentication    Chat Service    Memory Service
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
Conversation     Embedding        Prompt Builder
 History           Service
      │                │                │
      └────────────────┼────────────────┘
                       ▼
              Semantic Search (pgvector)
                       │
                       ▼
                 Google Gemini
                       │
                       ▼
             Store Chat Messages
                       │
                       ▼
                 AI Generated Response
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
| Phase 7 – Intelligent Memory Management | 🚀 Next |
| Phase 8 – Document Intelligence | ⏳ Planned |
| Phase 9 – Multimodal AI | ⏳ Planned |
| Phase 10 – Decision Intelligence Engine | ⏳ Planned |

---

# 🎯 Upcoming Features (Phase 7)

The next phase focuses on making the assistant smarter by automatically understanding, organizing, and managing user memories.

### Planned Features

- Automatic Memory Extraction
- Intelligent Memory Ranking
- Context Window Management
- Memory Summarization
- Token Optimization
- Intelligent Context Selection
- Improved Retrieval Accuracy
- Enhanced Personalization

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
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Conversational RAG
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
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Conversational AI
- Large Language Models (LLMs)
- Production Architecture
- Cloud-ready Development

The long-term vision is to build an intelligent assistant capable of:

- Understanding user memories
- Maintaining long-term semantic memory
- Preserving short-term conversational context
- Retrieving relevant information intelligently
- Assisting with decisions
- Learning user preferences
- Providing personalized, context-aware interactions

Future phases will extend the assistant with document intelligence, multimodal AI, automatic memory extraction, knowledge graphs, and intelligent decision-making capabilities.

---

# 📄 License

This project is being developed for educational purposes, portfolio development, and practical learning in:

- Software Engineering
- Artificial Intelligence
- Machine Learning
- Full Stack Development
- Distributed Systems
- Large Language Models
- Retrieval-Augmented Generation
- Conversational AI