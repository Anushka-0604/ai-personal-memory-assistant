# Phase 6 – Conversational AI & Chat Management

## Overview

In the previous phases, we built the core backend of our AI Personal Memory & Decision Assistant, including secure authentication, memory CRUD operations, Machine Learning embedding generation, semantic search using pgvector, and Retrieval-Augmented Generation (RAG).

Although the assistant could answer questions using stored memories, it behaved like a simple question-answering system. It had no understanding of ongoing conversations, previous messages, or multiple chat sessions.

The objective of Phase 6 was to transform the assistant into a conversation-aware AI system capable of maintaining chat sessions, remembering previous interactions, and supporting natural multi-turn conversations similar to ChatGPT, Gemini, and Claude.

---

# Objectives

The main objectives of this phase were:

- Introduce chat sessions.
- Store complete conversation history.
- Support multi-turn conversations.
- Automatically save every user and assistant message.
- Improve session management.
- Optimize prompt construction.
- Reduce prompt size using a sliding conversation window.
- Handle LLM failures gracefully.
- Build a production-ready conversational backend.

---

# Module 1 – Chat Sessions

## Problem

Previously, every request was treated as an independent question. There was no concept of a continuous conversation.

## Solution

A new **Chat Session** system was introduced.

Each user can now create multiple chat sessions, allowing conversations to remain independent and organized.

### Features Implemented

- Create Chat Session
- Retrieve Chat Sessions
- Retrieve Individual Chat Session
- Delete Chat Session

### Database

A new **ChatSession** table was created containing:

- id
- user_id
- title
- created_at
- updated_at

---

# Module 2 – Chat Messages

## Problem

Although sessions existed, messages were not permanently stored.

## Solution

A new **ChatMessage** model was introduced.

Each message stores:

- session_id
- role (user or assistant)
- content
- created_at

### Features Implemented

- Store user messages.
- Store assistant responses.
- Retrieve complete conversation history.

This allows every conversation to be permanently stored in the database.

---

# Module 3 – Conversation History Integration

## Problem

The assistant answered only using stored memories and completely forgot previous questions.

Example:

User:
What is my favourite programming language?

Assistant:
Python.

User:
Why do I like it?

Without previous conversation history, the assistant could not understand what "it" referred to.

## Solution

Conversation history is now automatically loaded before generating every response.

The prompt now contains:

- Previous Conversation
- Relevant Memories
- Current User Question

This enables the assistant to understand follow-up questions and maintain conversational context.

---

# Module 4 – Automatic Conversation Persistence

## Problem

Messages previously required separate API calls to be stored.

## Solution

The chat endpoint now automatically performs the following operations:

1. Save user message.
2. Load previous conversation.
3. Retrieve relevant memories.
4. Build prompt.
5. Generate AI response.
6. Save assistant response.
7. Return final response.

This removes the need for manually storing conversation messages.

---

# Module 5 – Smart Session Management

## Recent Activity Ordering

Whenever a new message is created, the session's **updated_at** timestamp is automatically updated.

This ensures the most recently active conversations always appear at the top of the chat list.

## Rename Chat Session

Implemented support for renaming existing conversations.

Endpoint:

PUT /chat/sessions/{id}

## Security

Ownership validation ensures that users can modify only their own chat sessions.

---

# Module 6 – Production Optimizations

## Sliding Conversation Window

Instead of sending the complete conversation to the LLM, only the most recent messages are included in the prompt.

This significantly reduces:

- Prompt size
- API cost
- Response latency
- Token usage

Older messages remain stored in the database.

---

## Configurable History Length

The conversation history limit is now configurable through:

- config.py
- .env

Changing the conversation window no longer requires modifying application code.

---

## Improved Prompt Engineering

The prompt was redesigned with clear instructions for the LLM.

The assistant is instructed to:

- Use memories as the primary source.
- Use previous conversation only for context.
- Never fabricate information.
- Clearly indicate when information is unavailable.
- Respond naturally and accurately.

---

## Graceful LLM Fallback

Exception handling was added around Gemini API calls.

If the LLM becomes unavailable, the assistant returns a friendly fallback message instead of crashing.

This improves reliability and user experience.

---

# Testing

Successfully tested:

- User Authentication
- JWT Authorization
- Chat Session Creation
- Chat Session Retrieval
- Memory CRUD
- Embedding Generation
- Semantic Search
- Automatic Message Storage
- Session Ordering
- Rename Chat Session

---

# Pending Validation

The following features were successfully implemented but could not be fully validated because the Gemini API returned:

HTTP 429 RESOURCE_EXHAUSTED (Quota Exceeded)

Pending validation includes:

- AI-generated responses using retrieved memories.
- Multi-turn conversation understanding.
- Unknown-information handling.

The implementation is complete. These tests will be rerun once Gemini API quota becomes available.

---

# Technologies Used

Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic

Machine Learning

- Sentence Transformers
- all-MiniLM-L6-v2
- pgvector
- Cosine Similarity Search

Artificial Intelligence

- Google Gemini API
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering

Security

- JWT Authentication
- OAuth2
- Password Hashing
- Protected APIs

---

# Architecture After Phase 6

The application workflow is now:

User

↓

JWT Authentication

↓

Create / Select Chat Session

↓

Ask Question

↓

Save User Message

↓

Load Conversation History

↓

Semantic Search

↓

Retrieve Relevant Memories

↓

Prompt Builder

↓

Gemini LLM

↓

Save Assistant Response

↓

Return Final Answer

---

# Deferred Feature

One feature was intentionally postponed.

## Automatic Memory Extraction

Current behaviour:

The user manually creates memories using the Memory API.

Future behaviour:

The assistant will automatically detect important information from conversations, generate embeddings, and store them as long-term memories without requiring manual API calls.

This feature will be implemented in a future phase.

---

# Phase Summary

Phase 6 transformed the project from a memory-based Retrieval-Augmented Generation system into a complete conversation-aware AI assistant.

The assistant now supports:

- Multiple chat sessions.
- Persistent conversation history.
- Context-aware conversations.
- Automatic conversation persistence.
- Smart session management.
- Sliding conversation windows.
- Optimized prompt engineering.
- Graceful LLM failure handling.

This phase completed the conversational AI foundation required for building an intelligent AI-powered Second Brain.

---

# Next Phase

The next phase focuses on **Document Intelligence**.

The assistant will be extended to process uploaded documents such as PDFs, DOCX files, and TXT files by:

- Extracting text.
- Splitting documents into chunks.
- Generating embeddings.
- Storing embeddings in PostgreSQL using pgvector.
- Performing semantic search across documents.
- Combining retrieved document chunks with personal memories.
- Using Retrieval-Augmented Generation (RAG) to answer questions from both memories and uploaded documents.

This will transform the assistant into a true AI-powered Second Brain capable of understanding both manually stored memories and uploaded knowledge sources.