# Database Schema

The AI Personal Memory & Decision Assistant currently uses PostgreSQL as its primary relational database.

The database contains two tables:

- users
- memories

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
| created_at | Timestamp | Memory Creation Time |
| updated_at | Timestamp | Last Updated Time |

---

# Entity Relationship

```
User (1)

│

├───────────────┐
│               │
│               │
▼               ▼

Memory 1     Memory 2

Memory 3     Memory 4
```

One User can have multiple Memories.

Each Memory belongs to exactly one User.

---

# Current Database Structure

```
PostgreSQL

│

├── users

└── memories
```

---

# Future Database Expansion

Upcoming tables may include:

- memory_embeddings
- conversations
- uploaded_documents
- uploaded_images
- voice_memories
- decision_history

These will support:

- Semantic Search
- Retrieval-Augmented Generation (RAG)
- AI Personal Assistant
- Knowledge Graph