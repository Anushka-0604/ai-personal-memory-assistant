# System Architecture

## Overview

The AI Personal Memory & Decision Assistant is a production-level AI application designed to act as a secure digital second brain. The system allows users to upload, organize, search, and interact with their personal knowledge using modern Artificial Intelligence techniques.

The application follows a modular microservice-inspired architecture to ensure scalability, maintainability, and security.

---

# High-Level Architecture

```
                        User
                          │
                          ▼
                React Frontend (TypeScript)
                          │
                    REST API / HTTPS
                          │
                          ▼
                FastAPI Backend (Python)
                          │
      ┌─────────────┬──────────────┬───────────────┐
      │             │              │               │
      ▼             ▼              ▼               ▼
 PostgreSQL      Qdrant         Neo4j          File Storage
(User Data)   (Embeddings)  (Knowledge Graph) (Documents)

                          │
                          ▼
                Large Language Model (LLM)
```

---

# Major Components

## Frontend

Technology:
- React
- TypeScript
- Tailwind CSS

Responsibilities:

- User Authentication
- Dashboard
- Chat Interface
- Document Upload
- Settings
- User Profile

---

## Backend

Technology:

- Python
- FastAPI

Responsibilities:

- Authentication
- API Development
- AI Integration
- Document Processing
- Database Communication
- File Management

---

## PostgreSQL

Stores:

- User Accounts
- Chat History
- Metadata
- Document Information
- Application Settings

---

## Qdrant

Stores:

- Vector Embeddings
- Semantic Representations
- Search Index

Used for:

- Semantic Search
- Retrieval-Augmented Generation (RAG)

---

## Neo4j

Stores:

- Entities
- Relationships
- Knowledge Graph

Used for:

- Context Discovery
- Relationship Analysis
- Connected Knowledge

---

## Large Language Model (LLM)

Responsible for:

- Question Answering
- Summarization
- Decision Support
- Context-Aware Responses

---

# Data Flow

1. User uploads a document.
2. Backend extracts the document text.
3. Text is divided into chunks.
4. Embeddings are generated.
5. Embeddings are stored in Qdrant.
6. Metadata is stored in PostgreSQL.
7. Relationships are stored in Neo4j.
8. During chat, relevant information is retrieved.
9. The LLM generates a context-aware response.

---

# Deployment

Development:

- Windows 11
- Docker Desktop
- PostgreSQL
- VS Code

Production (Planned):

- AWS
- Docker
- HTTPS
- Cloud Storage

---

# Future Enhancements

- Multi-user collaboration
- Voice interaction
- Mobile application
- Calendar integration
- Email integration
- Local LLM support