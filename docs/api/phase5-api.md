# Phase 5 API Documentation

## Overview

Phase 5 introduces the AI Chat API, enabling Retrieval-Augmented Generation (RAG).

The endpoint retrieves relevant memories from the vector database and uses them as context for the Large Language Model before generating a response.

---

# POST /chat

## Description

Answers a user's question using semantic memory retrieval and a Large Language Model.

Authentication Required:

Yes (JWT Bearer Token)

---

## Request Body

```json
{
    "question": "What do I have tomorrow?",
    "top_k": 5
}
```

---

## Parameters

| Field | Type | Description |
|--------|------|-------------|
| question | string | User's question |
| top_k | integer | Maximum number of memories to retrieve |

---

## Success Response

```json
{
    "answer": "You have an interview tomorrow at 10 AM.",
    "retrieved_memories": [
        {
            "id": 1,
            "content": "I have an interview tomorrow at 10 AM.",
            "source": "manual",
            "similarity": 0.3588
        }
    ]
}
```

---

## Response Fields

| Field | Description |
|--------|-------------|
| answer | AI-generated response |
| retrieved_memories | Memories used to answer the question |

---

## Error Handling

The endpoint gracefully handles:

- Gemini API quota exceeded
- Gemini API unavailable
- Unexpected LLM errors

Instead of returning an Internal Server Error (500), the API returns a meaningful fallback response.

Example:

```json
{
    "answer": "I couldn't generate a final AI response because the LLM is currently unavailable. However, I found relevant memories that may help.",
    "retrieved_memories": [
        {
            "id": 1,
            "content": "I have an interview tomorrow at 10 AM.",
            "source": "manual",
            "similarity": 0.3588
        }
    ]
}
```

---

# Internal Flow

Client
↓

POST /chat
↓

Generate Query Embedding
↓

Semantic Search (pgvector)
↓

Retrieve Top-K Memories
↓

Similarity Filtering
↓

Prompt Construction
↓

Gemini API
↓

Return Response