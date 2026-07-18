# Database Schema

The AI Personal Memory & Decision Assistant uses **PostgreSQL** as its primary relational database. Vector embeddings are stored using the **pgvector** extension, allowing semantic search directly within PostgreSQL.

After Phase 6, the database contains four main tables:

- users
- memories
- chat_sessions
- chat_messages

---

# Users Table

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| name | String | User Name |
| email | String | Unique Email Address |
| hashed_password | String | bcrypt Hashed Password |

---

# Memories Table

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id) |
| content | Text | Memory Content |
| source | String | Source of Memory |
| embedding | Vector(384) | Semantic Embedding (pgvector) |
| created_at | Timestamp | Memory Creation Time |
| updated_at | Timestamp | Last Updated Time |

---

# Chat Sessions Table

The **chat_sessions** table stores individual conversations created by users.

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id) |
| title | String | Chat Session Title |
| created_at | Timestamp | Session Creation Time |
| updated_at | Timestamp | Last Activity Time |

---

# Chat Messages Table

The **chat_messages** table stores every message exchanged between the user and the AI assistant.

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| session_id | Integer | Foreign Key (chat_sessions.id) |
| role | String | user / assistant |
| content | Text | Message Content |
| created_at | Timestamp | Message Creation Time |

---

# Entity Relationships

### User → Memory

**Relationship:** One-to-Many

One user can have multiple memories.

Each memory belongs to exactly one user.

---

### User → Chat Session

**Relationship:** One-to-Many

One user can create multiple chat sessions.

Each chat session belongs to exactly one user.

---

### Chat Session → Chat Message

**Relationship:** One-to-Many

One chat session contains multiple chat messages.

Each chat message belongs to exactly one chat session.

---

# Current Database Structure

```
PostgreSQL
│
├── users
├── memories
├── chat_sessions
└── chat_messages
```

---

# Database Architecture

```
                    User
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
    Memories                 Chat Sessions
        │                           │
        │                           ▼
        │                    Chat Messages
        │
        ▼
Vector Embeddings
(pgvector)
```

---

# Conversation Storage Workflow

Whenever the user interacts with the AI assistant, the following process occurs:

1. The user sends a message.
2. A new chat message is stored.
3. Previous conversation history is retrieved.
4. Relevant memories are retrieved using semantic search.
5. A prompt is constructed.
6. The LLM generates a response.
7. The assistant's response is stored as another chat message.

This design ensures that every conversation is permanently stored while also enabling context-aware interactions.

---

# Database Advantages

The current database design provides:

- Secure user management.
- Persistent personal memories.
- Semantic search using pgvector.
- Multi-session conversations.
- Complete conversation history.
- Context-aware AI interactions.
- Scalable relational database architecture.

---

# Future Database Expansion

Future phases may introduce additional tables such as:

- uploaded_documents
- document_chunks
- document_embeddings *(if a separate document storage strategy is adopted)*
- uploaded_images
- voice_memories
- decision_history
- knowledge_graph_nodes
- knowledge_graph_edges

These additions will support:

- Document Intelligence
- Document Semantic Search
- Retrieval-Augmented Generation (RAG)
- AI Personal Assistant
- Knowledge Graph
- Long-Term Memory Management