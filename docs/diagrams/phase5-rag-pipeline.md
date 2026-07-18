# Phase 5 RAG Pipeline

## Overview

Phase 5 introduced Retrieval-Augmented Generation (RAG) into the AI Personal Memory & Decision Assistant.

Instead of answering questions solely using the Large Language Model's general knowledge, the assistant first retrieves relevant memories from the user's personal vector database and uses them as context to generate accurate and personalized responses.

With the completion of **Phase 6**, the RAG pipeline has been enhanced by incorporating **conversation history**, allowing the assistant to maintain context across multiple interactions and answer follow-up questions naturally.

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
          Conversation History
                       │
                       ▼
            Prompt Construction
                       │
                       ▼
              Prompt Builder
      (Memories + History + Instructions)
                       │
                       ▼
               Gemini LLM
                       │
                       ▼
          AI Generated Response
                       │
                       ▼
         Store Chat Messages
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

## Step 5 — Conversation History

Recent messages from the current chat session are retrieved.

This provides the assistant with short-term conversational memory, enabling it to understand follow-up questions and maintain context throughout the conversation.

---

## Step 6 — Prompt Construction

The Prompt Builder combines:

- System instructions
- Retrieved semantic memories
- Recent conversation history
- User question

into a structured prompt for the LLM.

---

## Step 7 — Large Language Model

The prompt is sent to Google's Gemini API.

Gemini generates a grounded response using both retrieved memories and conversation history as context.

---

## Step 8 — Response Generation

The backend:

- Returns the AI-generated answer
- Stores both the user message and assistant response
- Preserves the conversation for future interactions

---

# Components Used

- FastAPI
- PostgreSQL
- pgvector
- Sentence Transformers
- all-MiniLM-L6-v2
- Google Gemini
- SQLAlchemy
- Chat Service
- Prompt Builder
- Chat Session Service
- Chat Message Service

---

# Advantages of the RAG Pipeline

- Reduces hallucinations
- Uses personal memories as context
- Maintains conversation context
- Produces personalized responses
- Supports multi-turn conversations
- Supports semantic search
- Easily scalable for larger memory collections

---

# Current Capabilities

The RAG pipeline now supports:

- Long-term semantic memory retrieval
- Short-term conversation history
- Session-based conversations
- Multi-turn dialogue
- Prompt engineering
- Context-aware AI responses
- Persistent chat history

---

# Future Enhancements

Future phases may introduce:

- Automatic memory extraction
- Intelligent memory ranking
- Context window optimization
- Document-aware RAG
- Voice-aware RAG
- Image-aware RAG
- Knowledge Graph integration