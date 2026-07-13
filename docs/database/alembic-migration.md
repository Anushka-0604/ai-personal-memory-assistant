# Alembic Migration History

This document records all database schema changes managed using Alembic.

---

# Migration 1

## Name

Create Users Table

### Description

Created the initial `users` table.

### Columns Added

- id
- name
- email

---

# Migration 2

## Name

Add Hashed Password

### Description

Added secure password storage to the users table.

### Columns Added

- hashed_password

---

# Migration 3

## Name

Create Memories Table

### Description

Introduced the Memory Engine database structure.

Created the `memories` table and established a relationship with the `users` table.

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

Whenever the database schema changes:

```
Update SQLAlchemy Models

↓

Generate Alembic Migration

↓

Review Migration File

↓

Run

alembic upgrade head

↓

Verify Changes in PostgreSQL
```

---

# Next Planned Migration

Phase 4

The next migration will introduce support for semantic search by adding an embedding column to the memories table.

Planned changes:

- Enable pgvector extension
- Add embedding column
- Create vector index