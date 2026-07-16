# Phase 5 – Retrieval-Augmented Generation (RAG) Chat System

## Objective

The goal of Phase 5 was to transform the AI Personal Memory Assistant from a memory storage system into an intelligent conversational assistant.

Instead of answering solely from the Large Language Model's general knowledge, the assistant now retrieves relevant memories from the user's personal memory database and uses them to generate grounded, personalized responses.

This architecture follows the Retrieval-Augmented Generation (RAG) approach.

---

# Features Implemented

## 1. Chat Endpoint

Implemented a new authenticated endpoint:

POST /chat

The endpoint accepts:

- User question
- Number of memories to retrieve (top_k)

Example Request

```json
{
    "question": "What do I have tomorrow?",
    "top_k": 5
}
```

---

## 2. Query Embedding Generation

Every incoming user question is converted into a dense vector embedding using:

SentenceTransformer
Model:
all-MiniLM-L6-v2

These embeddings enable semantic search instead of traditional keyword matching.

---

## 3. Semantic Memory Retrieval

Implemented semantic search using PostgreSQL pgvector.

Process:

User Question
↓

Generate Embedding
↓

Cosine Similarity Search
↓

Retrieve Top-K Memories

Each retrieved memory receives a similarity score.

---

## 4. Prompt Construction

A dedicated Prompt Builder combines:

- System instructions
- Retrieved memories
- User question

This creates a structured prompt for the Large Language Model.

---

## 5. Gemini Integration

Integrated Google's Gemini API through a dedicated LLMService.

Responsibilities:

- Send prompts
- Receive responses
- Handle API communication
- Keep LLM logic isolated from business logic

---

## 6. Chat Service

Implemented ChatService to orchestrate the complete RAG pipeline.

Responsibilities:

- Retrieve memories
- Filter relevant memories
- Build prompts
- Call the LLM
- Return the final response

---

## 7. Similarity Filtering

Implemented configurable similarity threshold filtering.

Only memories above the configured similarity threshold are used for response generation.

---

## 8. Error Handling

Implemented graceful handling of:

- Gemini API failures
- API quota exceeded
- Unexpected exceptions

Instead of crashing, the backend returns a meaningful fallback response.

---

## 9. Logging

Replaced temporary debugging statements with Python logging.

Benefits:

- Better debugging
- Production-ready logging
- Cleaner console output

---

# Phase 5 Architecture

User Question
↓

Generate Query Embedding
↓

Semantic Vector Search
↓

Top-K Relevant Memories
↓

Prompt Builder
↓

Gemini LLM
↓

AI Generated Response

---

# Technologies Used

- FastAPI
- PostgreSQL
- pgvector
- Sentence Transformers
- all-MiniLM-L6-v2
- Google Gemini API
- SQLAlchemy
- JWT Authentication

---

# Outcome

By the end of Phase 5, the backend supports:

- AI-powered question answering
- Semantic memory retrieval
- Retrieval-Augmented Generation (RAG)
- Prompt engineering
- LLM integration
- Graceful API failure handling

The project now functions as a complete basic RAG-powered AI Personal Memory Assistant.

---

# Next Phase

Phase 6 will introduce:

- Automatic memory extraction
- Conversation history
- Session-based conversations
- Short-term conversational memory
- Combined short-term and long-term memory