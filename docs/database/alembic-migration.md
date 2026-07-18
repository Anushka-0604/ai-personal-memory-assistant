# Alembic Migration History

This document records all database schema changes managed using Alembic throughout the development of the AI Personal Memory & Decision Assistant.

---

# Migration 1

## Name

Create Users Table

### Description

Created the initial `users` table to store user account information.

### Columns Added

- id
- name
- email

---

# Migration 2

## Name

Add Hashed Password

### Description

Added secure password storage to the `users` table using bcrypt hashing.

### Columns Added

- hashed_password

---

# Migration 3

## Name

Create Memories Table

### Description

Introduced the Memory Engine by creating the `memories` table and establishing a relationship with the `users` table.

### Columns Added

- id
- user_id
- content
- source
- created_at
- updated_at

### Foreign Key

```
user_id
    ↓
users.id
```

### Relationship

```
One User
    ↓
Many Memories
```

---

# Migration 4

## Name

Enable Vector Search

### Description

Enabled the **pgvector** extension and added support for semantic search by introducing an embedding column to the `memories` table.

### Changes

- Enabled pgvector extension
- Added embedding column
- Configured vector storage for semantic search

### Columns Added

- embedding (Vector(384))

---

# Migration 5

## Name

Create Chat Sessions Table

### Description

Added support for persistent conversations by creating the `chat_sessions` table.

### Columns Added

- id
- user_id
- title
- created_at
- updated_at

### Foreign Key

```
user_id
    ↓
users.id
```

### Relationship

```
One User
    ↓
Many Chat Sessions
```

---

# Migration 6

## Name

Create Chat Messages Table

### Description

Added the `chat_messages` table to permanently store every conversation between the user and the AI assistant.

### Columns Added

- id
- session_id
- role
- content
- created_at

### Foreign Key

```
session_id
      ↓
chat_sessions.id
```

### Relationship

```
One Chat Session
        ↓
Many Chat Messages
```

---

# Current Database Version

Current Migration

```
head
```

Status

```
Up to date
```

---

# Migration Workflow

Whenever the database schema changes, the following workflow is followed:

```
Update SQLAlchemy Models
        │
        ▼
Generate Alembic Migration
        │
        ▼
Review Migration File
        │
        ▼
Run

alembic upgrade head

        │
        ▼
Verify Changes in PostgreSQL
```

---

# Migration Summary

| Migration | Purpose |
|-----------|---------|
| Migration 1 | Create Users Table |
| Migration 2 | Add Secure Password Storage |
| Migration 3 | Create Memories Table |
| Migration 4 | Enable pgvector & Add Embeddings |
| Migration 5 | Create Chat Sessions Table |
| Migration 6 | Create Chat Messages Table |

---

# Future Migrations

Future phases may introduce additional migrations for:

- Uploaded Documents
- Document Chunks
- Document Embeddings (if required)
- Image Storage
- Voice Memories
- Decision History
- Knowledge Graph Integration
- Automatic Memory Extraction

These migrations will further extend the database while maintaining version control through Alembic.