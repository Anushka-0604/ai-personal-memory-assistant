# AI Architecture

**Project:** AI Personal Memory & Decision Assistant

**Module:** Artificial Intelligence

**Architecture Version:** v0.4.0

**Last Updated:** After Phase 4

---

# Overview

The Artificial Intelligence layer is responsible for enabling semantic understanding and intelligent retrieval of user memories.

Unlike traditional applications that rely on exact keyword matching, the AI layer converts every memory into a dense numerical representation called an **embedding**. These embeddings capture the semantic meaning of the stored information, allowing the application to retrieve memories based on intent and context rather than exact wording.

At the end of Phase 4, the AI subsystem consists of:

- Embedding Generation
- Vector Storage
- Semantic Search
- Retrieval Engine

Future phases will extend this architecture by integrating Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), decision-making modules, and long-term memory management.

---

# AI Layer Overview

```
                   User

                     │

                     ▼

            Natural Language

                     │

                     ▼

          Embedding Generation

                     │

                     ▼

            Dense Vector (384)

                     │

                     ▼

        PostgreSQL + pgvector

                     │

                     ▼

          Semantic Retrieval

                     │

                     ▼

         Relevant Memories
```

---

# AI Pipeline

The AI pipeline transforms human language into machine-understandable vector representations.

```
Text

↓

Sentence Transformer

↓

Embedding

↓

Vector Database

↓

Similarity Search

↓

Relevant Memories
```

---

# AI Components

## 1. Embedding Service

Location

```
backend/app/services/embedding_service.py
```

Responsibilities

- Load the embedding model
- Generate embeddings
- Convert vectors into Python lists
- Provide a reusable interface for other services

The model is loaded only once during application startup to reduce inference time.

---

## 2. Embedding Model

Current model

```
all-MiniLM-L6-v2
```

Framework

```
Sentence Transformers
```

Backend

```
PyTorch
```

Output

```
384-dimensional embedding
```

---

# Why This Model?

The selected model provides an excellent balance between:

- Speed
- Accuracy
- Memory usage
- Inference latency

Advantages

- Open source
- Lightweight
- Fast inference
- Excellent semantic retrieval
- Production proven
- Small memory footprint

---

# Embedding Generation Workflow

```
Memory Text

↓

SentenceTransformer

↓

Tokenizer

↓

Transformer Encoder

↓

Pooling Layer

↓

384-Dimensional Embedding
```

Example

Input

```
"I have an interview tomorrow."
```

Output

```
[-0.0803,
 0.0895,
 ...
 384 floating point values]
```

---

# Storage Layer

Generated embeddings are stored inside PostgreSQL using pgvector.

Database

```
PostgreSQL 17
```

Extension

```
pgvector
```

Schema

```
embedding VECTOR(384)
```

This enables SQL queries to perform semantic similarity search.

---

# Automatic Embedding Generation

Whenever a new memory is created:

```
POST /memories

↓

Generate Embedding

↓

Store Memory

+

Store Embedding
```

No additional user interaction is required.

---

# Automatic Embedding Updates

Whenever a memory changes:

```
PUT /memories/{id}

↓

Generate New Embedding

↓

Replace Previous Vector
```

This ensures that embeddings always reflect the latest memory content.

---

# Semantic Search Engine

Instead of keyword matching, the AI layer performs vector similarity search.

Workflow

```
User Query

↓

Generate Query Embedding

↓

Cosine Similarity

↓

Nearest Embeddings

↓

Top-K Memories
```

---

# Similarity Metric

Current metric

```
Cosine Similarity
```

Reason

Cosine similarity compares the orientation of vectors rather than their magnitude, making it highly effective for sentence embeddings.

Similarity

```
1.0

↓

Nearly identical meaning
```

Similarity

```
0

↓

Unrelated meaning
```

---

# AI Retrieval Pipeline

```
Question

↓

Embedding

↓

Vector Database

↓

Top-K Retrieval

↓

Relevant Memories
```

At the end of Phase 4, the pipeline stops after retrieving the most relevant memories.

---

# Current AI Architecture

```
                 User

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

        384-D Embedding

                   │

                   ▼

      PostgreSQL + pgvector

                   │

                   ▼

        Semantic Search
```

---

# AI Data Flow

## Memory Creation

```
Memory

↓

Embedding

↓

Database
```

---

## Memory Update

```
Updated Memory

↓

New Embedding

↓

Database
```

---

## Semantic Search

```
Question

↓

Embedding

↓

Cosine Similarity

↓

Relevant Memories
```

---

# Current Capabilities

The AI subsystem currently supports:

- Automatic embedding generation
- Dense vector representation
- Vector database storage
- Semantic similarity search
- Retrieval of relevant memories
- AI-ready backend architecture

---

# Limitations

The current implementation does not yet generate natural-language responses.

Instead, it retrieves relevant memories that will later be supplied to a Large Language Model.

---

# Phase 5 AI Architecture

Phase 5 introduces Retrieval-Augmented Generation.

```
User Question

↓

Embedding Generation

↓

Vector Search

↓

Relevant Memories

↓

Context Builder

↓

Prompt Builder

↓

Large Language Model

↓

Natural Language Response
```

The retrieval engine implemented in Phase 4 becomes the context provider for the LLM.

---

# Future AI Roadmap

The AI subsystem will gradually evolve to support:

## Phase 5

- Retrieval-Augmented Generation (RAG)
- LLM Integration
- Prompt Engineering
- Conversational Responses

## Phase 6

- Long-Term Memory Consolidation
- Memory Ranking
- Context Windows

## Phase 7

- Decision Engine
- Personalized Recommendations
- Context-Aware Planning

## Phase 8

- Multi-modal Memory
- Image Embeddings
- Document Embeddings
- Voice Memory

---

# Design Principles

The AI architecture follows several engineering principles.

### Modularity

Embedding generation is isolated inside a dedicated service.

### Reusability

The embedding service can be used by any future module.

### Scalability

The current architecture supports replacing the embedding model without changing business logic.

### Configurability

The embedding model is loaded from:

```
.env
```

instead of being hardcoded.

---

# Summary

The AI subsystem introduced in Phase 4 transforms the application from a traditional database-backed memory application into an intelligent semantic retrieval system.

By combining Sentence Transformers, PostgreSQL, pgvector, and cosine similarity search, the application now understands the meaning of user memories rather than relying on exact keyword matching.

This AI architecture establishes the retrieval foundation required for Retrieval-Augmented Generation and all future intelligent capabilities of the AI Personal Memory & Decision Assistant.