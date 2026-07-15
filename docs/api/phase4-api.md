# Phase 4 API Documentation

**Project:** AI Personal Memory & Decision Assistant

**Phase:** 4

**Status:** Stable

---

# Overview

Phase 4 introduces Artificial Intelligence capabilities into the backend by adding semantic memory retrieval.

The existing CRUD APIs remain unchanged. A new endpoint has been added that enables semantic search over stored memories using vector embeddings.

All memory operations continue to require JWT authentication.

---

# Authentication

All memory-related endpoints require a valid JWT access token.

Header:

```http
Authorization: Bearer <access_token>
```

---

# Existing Memory APIs

These APIs were retained from Phase 3.

| Method | Endpoint | Description |
|----------|-------------------------|--------------------------------------|
| POST | `/memories` | Create a new memory |
| GET | `/memories` | Retrieve all memories |
| GET | `/memories/{id}` | Retrieve a specific memory |
| PUT | `/memories/{id}` | Update a memory |
| DELETE | `/memories/{id}` | Delete a memory |

---

# Internal Changes

Although the API contract remains unchanged, the backend implementation has changed significantly.

Whenever a memory is created or updated:

1. The input text is sent to the embedding service.
2. A 384-dimensional vector is generated.
3. The vector is stored in PostgreSQL.
4. The API returns the normal response.

The client does not need to generate embeddings manually.

---

# New API

## POST /memories/search

Performs semantic search using vector similarity.

Instead of searching for exact keywords, this endpoint retrieves memories whose meanings are most similar to the user's query.

---

# Request

```http
POST /memories/search
Authorization: Bearer <token>
Content-Type: application/json
```

Body

```json
{
    "query": "What important work do I have tomorrow?",
    "top_k": 5
}
```

---

# Request Parameters

| Field | Type | Required | Description |
|---------|--------|-----------|----------------------------|
| query | string | Yes | User search query |
| top_k | integer | No | Maximum number of memories to return |

Default:

```
top_k = 5
```

---

# Response

```json
[
    {
        "id": 1,
        "content": "I have an interview tomorrow at 10 AM.",
        "source": "chat",
        "similarity": 0.9428
    }
]
```

---

# Response Fields

| Field | Type | Description |
|---------|----------|------------------------------------|
| id | integer | Memory ID |
| content | string | Stored memory text |
| source | string | Memory source |
| similarity | float | Semantic similarity score |

---

# Similarity Score

The similarity value ranges approximately between:

```
0.0 → unrelated

1.0 → highly similar
```

Higher values indicate stronger semantic similarity.

The score is calculated using cosine similarity over vector embeddings.

---

# Semantic Search Workflow

```
Client

↓

POST /memories/search

↓

FastAPI

↓

Generate Query Embedding

↓

pgvector Cosine Similarity

↓

Top K Memories

↓

JSON Response
```

---

# Example

Stored memory:

```
I have an interview tomorrow at 10 AM.
```

User searches:

```
What important work do I have tomorrow?
```

Traditional SQL search:

```
No Result
```

Semantic search:

```
Interview Memory Found
```

This demonstrates the primary advantage of vector search.

---

# Error Responses

## Unauthorized

```http
401 Unauthorized
```

Example

```json
{
    "detail": "Could not validate credentials"
}
```

---

## Validation Error

```http
422 Unprocessable Entity
```

Example

```json
{
    "detail": [
        ...
    ]
}
```

---

# Security

The endpoint only searches memories belonging to the authenticated user.

Internally:

```
WHERE user_id = current_user.id
```

Users cannot retrieve another user's memories.

---

# Performance

Current implementation:

- Generates one query embedding
- Computes cosine similarity
- Returns Top-K results

Future optimizations include:

- HNSW indexing
- IVFFlat indexing
- Approximate nearest neighbor search
- Hybrid keyword + vector search

---

# API Changes in Phase 4

## New Endpoint

```
POST /memories/search
```

## Existing Endpoint Enhancements

### POST /memories

Now automatically:

- Generates embeddings
- Stores vectors

### PUT /memories/{id}

Now automatically:

- Regenerates embeddings
- Updates stored vectors

No API contract changes were required for clients.

---

# Summary

Phase 4 extends the backend with semantic retrieval capabilities while maintaining full backward compatibility.

The API now supports:

- Automatic embedding generation
- Vector storage
- Semantic similarity search
- Retrieval-ready architecture

These APIs serve as the retrieval layer for Retrieval-Augmented Generation (RAG), which will be implemented in Phase 5.