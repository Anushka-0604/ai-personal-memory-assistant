# AI Architecture

**Project:** AI Personal Memory & Decision Assistant

**Module:** Artificial Intelligence

**Architecture Version:** v0.6.0

**Last Updated:** After Phase 6

---

# Overview

The Artificial Intelligence layer is responsible for enabling semantic understanding, intelligent retrieval, conversation management, and AI-powered response generation using the user's stored memories.

Unlike traditional applications that rely on exact keyword matching, the AI layer converts every memory into a dense numerical representation called an **embedding**. These embeddings capture the semantic meaning of stored information, allowing the application to retrieve memories based on intent and context rather than exact wording.

With the completion of **Phase 6**, the AI subsystem now combines:

- Long-term semantic memory
- Short-term conversation history
- Session-based conversations
- Embedding Generation
- Vector Storage
- Semantic Search
- Retrieval Engine
- Prompt Builder
- Retrieval-Augmented Generation (RAG)
- Gemini LLM Integration

The retrieval engine now combines **semantic memories** with **recent conversation history** before constructing prompts for the Large Language Model. This enables the assistant to understand follow-up questions, maintain conversational context, and generate personalized, memory-grounded responses.

Future phases will further extend this architecture with automatic memory extraction, document intelligence, voice intelligence, image understanding, and intelligent decision support.

---

# AI Layer Overview

```
                   User

                     │

                     ▼

            Natural Language

                     │

                     ▼

          Conversation History

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

         Top-K Memory Retrieval

                     │

                     ▼

            Prompt Builder
 (History + Memories + Instructions)

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

# AI Pipeline

The AI pipeline transforms human language into intelligent, context-aware responses using Retrieval-Augmented Generation (RAG).

```
User Question

↓

Retrieve Conversation History

↓

Generate Query Embedding

↓

Semantic Vector Search

↓

Top-K Relevant Memories

↓

Similarity Threshold

↓

Prompt Builder

↓

Gemini LLM

↓

Store Chat Messages

↓

AI Generated Response
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

## 3. Prompt Builder

Location

```
backend/app/services/prompt_builder.py
```

Responsibilities

- Construct structured prompts
- Combine retrieved semantic memories
- Combine recent conversation history
- Add system instructions
- Include the user's current question

The Prompt Builder now combines both **long-term memory** (retrieved semantic memories) and **short-term memory** (recent conversation history), enabling the Large Language Model to generate context-aware and personalized responses.

---

## 4. LLM Service

Location

```
backend/app/services/llm_service.py
```

Responsibilities

- Communicate with the Gemini API
- Submit prompts
- Receive generated responses
- Handle API failures gracefully

The LLM Service abstracts all communication with the external language model, keeping business logic independent of the chosen provider.

---

## 5. Chat Service

Location

```
backend/app/services/chat_service.py
```

Responsibilities

- Retrieve conversation history
- Perform semantic retrieval
- Filter relevant memories
- Build the final prompt
- Invoke the LLM
- Store conversation messages
- Return the final AI response

The Chat Service orchestrates the complete conversational Retrieval-Augmented Generation (RAG) pipeline.

---

## 6. Chat Session Service

Location

```
backend/app/services/chat_session_service.py
```

Responsibilities

- Create chat sessions
- Retrieve user chat sessions
- Rename chat sessions
- Delete chat sessions
- Manage session metadata

This service manages persistent conversations for every user.

---

## 7. Chat Message Service

Location

```
backend/app/services/chat_message_service.py
```

Responsibilities

- Store user messages
- Store AI responses
- Retrieve conversation history
- Maintain message ordering

This service provides the short-term conversational memory used by the AI assistant.

# Retrieval-Augmented Generation (RAG)

Phase 5 introduced Retrieval-Augmented Generation (RAG), enabling the assistant to answer questions using the user's stored memories instead of relying solely on the Large Language Model's pretrained knowledge.

With the completion of **Phase 6**, the RAG pipeline has evolved into a **conversational RAG system** by combining:

- Long-term semantic memory (retrieved memories)
- Short-term conversation history
- Current user question

This allows the assistant to maintain context across multiple interactions and answer follow-up questions naturally.

Benefits

- Personalized responses
- Reduced hallucinations
- Memory-grounded answers
- Better factual consistency
- Multi-turn conversations
- Context-aware reasoning
- Explainable retrieval process

---

# RAG Pipeline

```
User Question

↓

Retrieve Conversation History

↓

Generate Query Embedding

↓

Semantic Vector Search

↓

Top-K Relevant Memories

↓

Similarity Threshold Filter

↓

Prompt Builder
(History + Memories + Instructions)

↓

Gemini LLM

↓

AI Generated Response

↓

Store Chat Messages
```

---

# Prompt Construction

The Prompt Builder creates structured prompts using:

- System instructions
- Retrieved semantic memories
- Recent conversation history
- Current user question

Example

```
System:
You are an AI Personal Memory Assistant.

Conversation History:
User: I have an interview tomorrow.
Assistant: Got it.

Relevant Memories:
- Interview is tomorrow at 10 AM.

Current Question:
What time is it?

Answer:
```

Providing both **long-term semantic memory** and **short-term conversation history** enables the LLM to generate responses that are accurate, personalized, and context-aware.

---

# AI Retrieval Pipeline

```
Question

↓

Retrieve Conversation History

↓

Generate Query Embedding

↓

Vector Database

↓

Top-K Retrieval

↓

Conversation History
        +
Relevant Memories

↓

Prompt Builder

↓

Gemini LLM

↓

Store Chat Messages

↓

AI Response
```

# Current AI Architecture

```
                    User
                      │
                      ▼
                 Chat Service
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
Conversation    Embedding Service  Prompt Builder
 History             │                  │
      │              ▼                  ▼
      │      Sentence Transformer  Retrieved Memories
      │                                 │
      └───────────────┬─────────────────┘
                      ▼
                 Gemini LLM
                      │
                      ▼
            Store Chat Messages
                      │
                      ▼
             AI Generated Response
```

---

# AI Data Flow

## Memory Creation

```
Memory

↓

Generate Embedding

↓

Database
```

---

## Memory Update

```
Updated Memory

↓

Generate New Embedding

↓

Replace Existing Embedding

↓

Database
```

---

## AI Chat

```
Question

↓

Retrieve Conversation History

↓

Generate Query Embedding

↓

Semantic Search

↓

Retrieve Relevant Memories

↓

Prompt Builder

↓

Gemini

↓

Store Chat Messages

↓

AI Response
```

---

# Current Capabilities

The AI subsystem currently supports:

- Automatic embedding generation
- Automatic embedding updates
- Dense vector representation
- Vector database storage
- Semantic similarity search
- Retrieval of relevant memories
- Retrieval-Augmented Generation (RAG)
- Conversation history retrieval
- Session-based conversations
- Multi-turn dialogue
- Context-aware prompt construction
- Prompt engineering
- Gemini LLM integration
- AI-generated responses
- Persistent chat history
- Graceful LLM error handling
- Modular AI service architecture

---

# Current Limitations

Although the AI subsystem now supports conversational Retrieval-Augmented Generation, several advanced AI capabilities are intentionally deferred to future phases.

The current implementation does **not yet support**:

- Automatic memory extraction
- Intelligent memory ranking
- Context window optimization
- Memory summarization
- Token optimization
- Document-aware RAG
- Voice-aware RAG
- Image-aware RAG
- Knowledge Graph integration

---

# Future AI Roadmap

## Phase 7

Introduce more intelligent memory management by implementing:

- Automatic Memory Extraction
- Context Window Management
- Memory Ranking
- Memory Summarization
- Token Optimization
- Intelligent Context Selection

---

## Phase 8

Expand the assistant with document intelligence:

- Document Upload
- Text Extraction
- Chunking
- Document Embeddings
- Semantic Document Search
- Document-based RAG

---

## Phase 9

Expand beyond text with multimodal AI:

- Voice Memories
- Whisper Integration
- Voice Conversations
- Image Embeddings
- Image Understanding
- Cross-modal Retrieval

---

## Phase 10

Introduce intelligent reasoning capabilities:

- Decision Engine
- Personalized Recommendations
- Context-Aware Planning
- Goal Tracking
- Preference Learning
- Knowledge Graph Integration

---

# Design Principles

The AI architecture follows several engineering principles.

## Modularity

Each AI capability is implemented as an independent service.

Examples include:

- Embedding Service
- Prompt Builder
- LLM Service
- Chat Service
- Chat Session Service
- Chat Message Service

This minimizes coupling between components and simplifies maintenance.

---

## Reusability

Core AI services are reusable across multiple backend modules.

For example:

- Embedding generation is used for both memory creation and semantic search.
- Prompt Builder combines semantic memories and conversation history.
- Chat Service orchestrates the complete conversational RAG workflow.

---

## Scalability

The architecture is designed to support future improvements without major structural changes.

Examples include:

- Replacing the embedding model
- Switching from Gemini to another LLM
- Supporting multiple LLM providers
- Scaling to larger memory collections
- Adding document, voice, and image intelligence

---

## Configurability

AI-related configuration is externalized using environment variables.

Examples include:

```
EMBEDDING_MODEL

GEMINI_API_KEY

GEMINI_MODEL

RAG_SIMILARITY_THRESHOLD
```

This allows configuration changes without modifying application code.

---

## Separation of Responsibilities

Each service has a clearly defined responsibility.

| Service | Responsibility |
|----------|----------------|
| Embedding Service | Generate vector embeddings |
| Memory Service | Store and retrieve memories |
| Prompt Builder | Construct prompts using memories and conversation history |
| LLM Service | Communicate with Gemini |
| Chat Service | Coordinate the conversational RAG pipeline |
| Chat Session Service | Manage chat sessions |
| Chat Message Service | Store and retrieve conversation history |

This design improves readability, testing, and long-term maintainability.

---

# Summary

The AI subsystem has evolved from a semantic retrieval engine into a **conversational Retrieval-Augmented Generation (RAG)** system.

By combining:

- Sentence Transformers
- PostgreSQL
- pgvector
- Semantic Vector Search
- Conversation History
- Prompt Engineering
- Google Gemini

the application can retrieve relevant personal memories, maintain conversational context, and generate accurate, personalized responses.

With the completion of **Phase 6**, the assistant now supports persistent chat sessions, multi-turn conversations, and context-aware AI interactions while preserving the modular architecture required for future expansion.

Future phases will build upon this foundation by introducing automatic memory extraction, document intelligence, multimodal AI, knowledge graphs, and intelligent decision-making capabilities.
