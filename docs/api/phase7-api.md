# Phase 7 API Documentation

**Project:** AI Personal Memory & Decision Assistant

**Phase:** Phase 7 – Advanced Memory Intelligence

**Version:** v0.7.0

---

# Overview

Phase 7 extends the backend APIs by introducing intelligent memory enrichment, hybrid retrieval, personalized search, long-term memory management, and AI analytics.

The existing Memory and Chat APIs were enhanced to support automatic metadata extraction, improved retrieval, and production-grade evaluation.

In addition, new analytics endpoints were introduced to monitor AI performance and retrieval quality.

---

# Updated Memory APIs

## Create Memory

```
POST /memories
```

### Description

Creates a new memory.

During creation the system automatically performs:

- Entity Extraction
- Temporal Extraction
- Memory Classification
- Importance Ranking
- Sentiment Analysis
- Tag Generation
- Knowledge Graph Generation
- Embedding Generation
- Duplicate Detection

If a duplicate memory is detected, the existing memory is reinforced instead of creating a new record.

---

## Update Memory

```
PUT /memories/{memory_id}
```

### Description

Updates an existing memory.

The system automatically regenerates:

- Embedding
- Category
- Importance
- Tags
- Sentiment
- Confidence
- Temporal Information
- Extracted Entities

---

## Search Memories

```
POST /memories/search
```

### Description

Performs intelligent hybrid retrieval using:

- Conversation Context
- Query Rewrite
- Semantic Search
- PostgreSQL Full-Text Search
- Metadata Filtering
- Cross Encoder Re-ranking
- Personalization
- Diversification

---

## Search Request

```json
{
    "query": "Where is my interview?",
    "top_k": 5,
    "conversation_history": [
        "I have an interview tomorrow."
    ]
}
```

---

## Search Response

Each retrieved memory now includes:

```json
{
    "memory_id": 1,
    "content": "...",
    "similarity": 0.91,
    "hybrid_score": 0.89,
    "cross_encoder_score": 0.93,
    "retrieval_score": 0.91,
    "personalization_score": 0.76,
    "importance_score": 0.88,
    "recency_score": 0.82,
    "interaction_score": 0.71,
    "final_score": 0.90
}
```

---

# Updated Chat API

## Chat

```
POST /chat
```

### Description

The conversational AI pipeline now performs:

1. Retrieve conversation history
2. Rewrite query
3. Hybrid retrieval
4. Cross Encoder reranking
5. Personalized ranking
6. Context selection
7. Prompt construction
8. Gemini response generation
9. Evaluation logging
10. Store chat messages

---

# Analytics APIs

Phase 7 introduces AI monitoring endpoints.

---

## Retrieval Quality

```
GET /analytics/retrieval-quality
```

Returns:

- Average similarity
- Average retrieved memories
- Average selected memories
- Average response length
- Response success rate

---

## Usage Dashboard

```
GET /analytics/usage-dashboard
```

Returns:

- Total requests
- Successful requests
- Failed requests
- Average response time
- Average similarity
- Average response length

---

## AI Dashboard

```
GET /analytics/ai-dashboard
```

Provides a unified dashboard including:

- Retrieval Quality
- Usage Statistics
- System Health
- Performance Metrics

---

# Memory Response Changes

Memory APIs now return additional metadata.

New fields include:

| Field | Description |
|--------|-------------|
| category | Automatically classified category |
| importance | Memory importance score |
| tags | Generated tags |
| sentiment | Sentiment label |
| confidence | Sentiment confidence |
| temporal_date | Extracted temporal information |
| extracted_data | Structured extracted entities |
| access_count | Retrieval count |
| last_accessed | Last retrieval timestamp |
| evidence_count | Memory reinforcement count |
| is_archived | Archive status |
| is_forgotten | Forgetting status |

---

# AI Evaluation

Every chat request automatically records:

- Retrieval Count
- Selected Memories
- Average Similarity
- Context Score
- Response Length
- Embedding Time
- Retrieval Time
- Ranking Time
- Context Selection Time
- Prompt Construction Time
- LLM Generation Time
- Total Execution Time

---

# Phase 7 API Improvements

Compared to Phase 6, the APIs now support:

- Automatic memory enrichment
- Knowledge graph generation
- Duplicate detection
- Long-term memory management
- Hybrid semantic and keyword retrieval
- Cross Encoder reranking
- Personalized retrieval
- Context-aware search
- AI evaluation logging
- Retrieval analytics
- AI performance dashboards

---

# Summary

Phase 7 significantly expands the backend API capabilities by introducing intelligent retrieval, automatic memory understanding, long-term memory management, and production-grade AI monitoring.

The APIs now support hybrid Retrieval-Augmented Generation (RAG), personalized ranking, analytics, and evaluation while maintaining compatibility with the existing Memory and Chat APIs.