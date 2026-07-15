# Phase 4 Architecture Diagrams

**Project:** AI Personal Memory & Decision Assistant

**Phase:** 4

---

# Overview

This document contains the architectural diagrams introduced during Phase 4.

The objective of Phase 4 was to transform the application from a traditional CRUD-based backend into an AI-powered semantic memory retrieval system.

---

# 1. High-Level Architecture

```text
                +----------------------+
                |      Frontend        |
                +----------+-----------+
                           |
                     HTTP REST API
                           |
                           ▼
                +----------------------+
                |      FastAPI         |
                |      Backend         |
                +----------+-----------+
                           |
          +----------------+----------------+
          |                                 |
          ▼                                 ▼
+----------------------+         +----------------------+
|  Authentication      |         |   Memory Service     |
| JWT Authentication   |         | Business Logic       |
+----------------------+         +----------+-----------+
                                            |
                                            ▼
                               +--------------------------+
                               |   Embedding Service      |
                               | Sentence Transformers    |
                               +-----------+--------------+
                                           |
                                           ▼
                               +--------------------------+
                               | all-MiniLM-L6-v2 Model   |
                               +-----------+--------------+
                                           |
                                           ▼
                               +--------------------------+
                               | 384-Dimensional Vector   |
                               +-----------+--------------+
                                           |
                                           ▼
                            +-------------------------------+
                            | PostgreSQL + pgvector         |
                            | users                         |
                            | memories                      |
                            | embeddings                    |
                            +-------------------------------+
```

---

# 2. Memory Creation Pipeline

```text
User

 │

 ▼

POST /memories

 │

 ▼

FastAPI

 │

 ▼

Memory Service

 │

 ▼

Embedding Service

 │

 ▼

Sentence Transformer

 │

 ▼

Generate 384-D Vector

 │

 ▼

Store in PostgreSQL
```

---

# 3. Database Storage

```text
                 Memory Record

+-----------------------------------------------------+
| id                                                  |
| user_id                                             |
| content                                             |
| source                                              |
| embedding (VECTOR 384)                              |
| created_at                                          |
| updated_at                                          |
+-----------------------------------------------------+
```

---

# 4. Embedding Generation Flow

```text
Raw Text

 │

 ▼

SentenceTransformer

 │

 ▼

Tokenization

 │

 ▼

Transformer Encoder

 │

 ▼

Sentence Embedding

 │

 ▼

384 Floating Point Numbers

 │

 ▼

Store in Database
```

---

# 5. Semantic Search Pipeline

```text
User Query

 │

 ▼

Generate Query Embedding

 │

 ▼

Query Vector

 │

 ▼

Cosine Similarity Search

 │

 ▼

pgvector

 │

 ▼

Nearest Memory Embeddings

 │

 ▼

Top K Results

 │

 ▼

JSON Response
```

---

# 6. Semantic Search Example

Stored memories

```text
1. I have an interview tomorrow.

2. Buy groceries.

3. My passport expires next month.
```

User asks

```text
What important work do I have tomorrow?
```

Pipeline

```text
Question

 │

 ▼

Embedding

 │

 ▼

Compare against

Interview Memory

Groceries

Passport

 │

 ▼

Highest Similarity

 │

 ▼

Interview Memory Returned
```

Although the query does not contain the word **interview**, semantic similarity identifies it correctly.

---

# 7. Embedding Lifecycle

```text
Create Memory

 │

 ▼

Generate Embedding

 │

 ▼

Store Vector

 │

 ▼

Update Memory

 │

 ▼

Regenerate Embedding

 │

 ▼

Replace Previous Vector
```

This guarantees that the stored vector always matches the latest memory content.

---

# 8. Search Workflow Inside PostgreSQL

```text
Query Embedding

 │

 ▼

VECTOR(384)

 │

 ▼

Cosine Distance

 │

 ▼

Sort by Distance

 │

 ▼

Top K Similar Memories
```

---

# 9. Phase 4 System Architecture

```text
                   User

                     │

                     ▼

              FastAPI Backend

                     │

      ┌──────────────┴──────────────┐

      ▼                             ▼

Authentication               Memory Service

                                    │

                                    ▼

                           Embedding Service

                                    │

                                    ▼

                     Sentence Transformer Model

                                    │

                                    ▼

                         384-Dimensional Vector

                                    │

                                    ▼

                        PostgreSQL + pgvector

                                    │

                                    ▼

                         Semantic Search Engine
```

---

# 10. End-to-End Retrieval Pipeline

```text
Question

 │

 ▼

Generate Embedding

 │

 ▼

Vector Search

 │

 ▼

Relevant Memories

 │

 ▼

Return to User
```

> **Note:** In Phase 4, the pipeline ends after retrieving relevant memories. In Phase 5, these retrieved memories will be passed to a Large Language Model (LLM) to generate natural-language responses.

---

# Summary

Phase 4 introduces a complete AI retrieval pipeline.

The architecture now supports:

- Automatic embedding generation
- Vector storage
- PostgreSQL + pgvector integration
- Semantic similarity search
- AI-ready retrieval layer
- Foundation for Retrieval-Augmented Generation (RAG)

These diagrams illustrate the complete data flow from memory creation to semantic retrieval and provide the architectural foundation for Phase 5.