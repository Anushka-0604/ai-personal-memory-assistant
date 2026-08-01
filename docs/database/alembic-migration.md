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

---

# Migration 7

## Name

Add Memory Metadata

### Description

Extended the `memories` table to support intelligent memory understanding and metadata enrichment.

### Columns Added

- category
- importance
- tags
- sentiment
- confidence
- temporal_date
- extracted_data
- access_count
- last_accessed

---

# Migration 8

## Name

Add Evidence Count

### Description

Added support for duplicate detection and memory reinforcement.

### Columns Added

- evidence_count

---

# Migration 9

## Name

Add Archive Support

### Description

Introduced long-term memory management by allowing memories to be archived automatically.

### Columns Added

- is_archived

---

# Migration 10

## Name

Add Forgetting Support

### Description

Extended long-term memory management by allowing archived memories to be marked as forgotten.

### Columns Added

- is_forgotten

---

# Migration 11

## Name

Create AI Request Logs Table

### Description

Created the `ai_request_logs` table to store AI evaluation, retrieval analytics, response metrics, and execution timings.

### Table Created

```
ai_request_logs
```

Stores

- Retrieval metrics
- Response statistics
- Similarity scores
- Context scores
- Execution timings
- AI evaluation data

---

# Migration 12

## Name

Create System Metrics Table

### Description

Created the `system_metrics` table for production monitoring and AI dashboard support.

### Table Created

```
system_metrics
```

Stores

- System metrics
- Performance values
- Dashboard statistics
- Monitoring information

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
        │
        ▼
Verify Application Functionality
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
| Migration 7 | Add Memory Metadata |
| Migration 8 | Add Evidence Count |
| Migration 9 | Add Archive Support |
| Migration 10 | Add Forgetting Support |
| Migration 11 | Create AI Request Logs Table |
| Migration 12 | Create System Metrics Table |

---

# Phase 7 Database Enhancements

Phase 7 introduced several major database improvements through Alembic migrations:

- Automatic memory metadata storage
- Long-term memory management
- Duplicate memory reinforcement
- Evidence tracking
- Memory archiving
- Forgetting strategy
- AI request logging
- System metrics collection
- Analytics infrastructure
- Production monitoring support

---

# Future Migrations

Future phases may introduce additional migrations for:

- Uploaded Documents
- Document Chunks
- Image Storage
- Voice Memories
- Decision History
- Planner Tasks
- Agent Memory
- Multi-modal Storage

These migrations will continue extending the database schema while maintaining version control through Alembic and ensuring backward compatibility.