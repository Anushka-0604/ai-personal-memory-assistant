# Phase 5 RAG Pipeline

## Overview

Phase 5 introduces Retrieval-Augmented Generation (RAG) into the AI Personal Memory Assistant.

Instead of answering questions solely using the Large Language Model's general knowledge, the assistant first retrieves relevant memories from the user's personal vector database and then uses those memories as context to generate an accurate and personalized response.

---

# High-Level Pipeline

```
                 User Question
                       │
                       ▼
        Generate Query Embedding
                       │
                       ▼
         Semantic Vector Search
                 (pgvector)
                       │
                       ▼
         Top-K Relevant Memories
                       │
                       ▼
         Similarity Threshold Filter
                       │
                       ▼
            Prompt Construction
                       │
                       ▼
              Prompt Builder
                       │
                       ▼
               Gemini LLM
                       │
                       ▼
          AI Generated Response
```

---

# Step-by-Step Workflow

## Step 1 — User Question

The user submits a question through the `/chat` endpoint.

Example:

```
What do I have tomorrow?
```

---

## Step 2 — Query Embedding

The question is converted into a dense vector using:

- Sentence Transformers
- all-MiniLM-L6-v2

This enables semantic understanding instead of keyword matching.

---

## Step 3 — Semantic Search

The generated embedding is compared against stored memory embeddings using pgvector.

Similarity is computed using cosine distance.

The database returns the Top-K most relevant memories.

---

## Step 4 — Similarity Filtering

Retrieved memories are filtered using a configurable similarity threshold.

Only sufficiently relevant memories are included in the prompt.

---

## Step 5 — Prompt Construction

The Prompt Builder combines:

- System instructions
- Retrieved memories
- User question

into a structured prompt for the LLM.

---

## Step 6 — Large Language Model

The prompt is sent to Google's Gemini API.

Gemini generates a grounded response using the retrieved memories as context.

---

## Step 7 — Response Generation

The backend returns:

- AI-generated answer
- Retrieved memories
- Similarity scores

to the client.

---

# Components Used

- FastAPI
- PostgreSQL
- pgvector
- Sentence Transformers
- all-MiniLM-L6-v2
- Google Gemini
- SQLAlchemy

---

# Advantages of the RAG Pipeline

- Reduces hallucinations
- Uses personal memories as context
- Produces personalized responses
- Supports semantic search
- Easily scalable for larger memory collections

---

# Current Limitations

Current implementation includes:

- Long-term semantic memory
- Semantic retrieval
- Prompt engineering

Future phases will add:

- Short-term conversation history
- Automatic memory extraction
- Session-based conversations
- Context window management
- Multi-turn dialogue support