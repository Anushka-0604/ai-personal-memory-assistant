# AI Architecture

**Project:** AI Personal Memory & Decision Assistant

**Module:** Artificial Intelligence

Architecture Version: v0.7.0

Last Updated: After Phase 7

---

# Overview

The Artificial Intelligence layer is responsible for enabling semantic understanding, intelligent retrieval, conversation management, and AI-powered response generation using the user's stored memories.

Unlike traditional applications that rely on exact keyword matching, the AI layer converts every memory into a dense numerical representation called an **embedding**. These embeddings capture the semantic meaning of stored information, allowing the application to retrieve memories based on intent and context rather than exact wording.

With the completion of **Phase 7**, the AI subsystem has evolved into a production-grade intelligent memory architecture that combines advanced memory understanding, hybrid retrieval, long-term memory management, personalization, observability, analytics, and Retrieval-Augmented Generation (RAG).

The AI subsystem now combines:

- Long-term semantic memory
- Short-term conversation history
- Automatic memory extraction
- Memory classification
- Metadata enrichment
- Knowledge graph generation
- Hybrid semantic + keyword retrieval
- Query rewriting
- Cross-encoder reranking
- Personalized retrieval
- Intelligent context selection
- Long-term memory management
- AI observability
- Retrieval analytics
- Evaluation dashboards
- Prompt Builder
- Google Gemini Integration

The retrieval engine now combines conversation history, semantic search, keyword search, metadata filtering, AI reranking, and personalized ranking before constructing prompts for the Large Language Model, enabling more accurate and context-aware responses.

Future phases will further extend this architecture with automatic memory extraction, document intelligence, voice intelligence, image understanding, and intelligent decision support.

---

# AI Layer Overview

                     User Query
                          │
                          ▼
              Conversation Context
                          │
                          ▼
          Context Retrieval Service
                          │
                          ▼
             Query Rewrite Service
                          │
                          ▼
              Hybrid Retrieval Engine
          (Semantic + Keyword + Metadata)
                          │
                          ▼
           Cross Encoder Re-ranking
                          │
                          ▼
             Personalization Engine
                          │
                          ▼
             Intelligent Context Selector
                          │
                          ▼
                 Prompt Builder
                          │
                          ▼
                   Google Gemini
                          │
                          ▼
               AI Generated Response
                          │
                          ▼
          Evaluation & Analytics Logging

---

# AI Pipeline

The AI pipeline transforms human language into intelligent, context-aware responses using Retrieval-Augmented Generation (RAG).

```
User Question

↓

Conversation Context

↓

Query Rewrite

↓

Generate Query Embedding

↓

Semantic Search

+

Keyword Search

↓

Hybrid Merge

↓

Cross Encoder Re-ranking

↓

Personalization

↓

Context Selection

↓

Prompt Builder

↓

Gemini LLM

↓

Store Chat Messages

↓

Evaluation Logging

↓

AI Response
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

Additional Phase 7 Responsibilities

- Rewrite search queries
- Perform hybrid retrieval
- Execute cross-encoder reranking
- Apply personalized ranking
- Perform context-aware retrieval
- Record AI evaluation metrics
- Log observability metrics
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
## 8. Query Rewrite Service
Location

backend/app/services/query_rewrite_service.py

Responsibilities

- Expand search queries
- Improve semantic retrieval
- Improve keyword retrieval

## 9. Cross Encoder Service
Location

backend/app/services/cross_encoder_service.py

Responsibilities

- AI reranking
- Cross-encoder scoring
- Improve retrieval precision

## 10. Personalization Service

Location

```
backend/app/services/personalization_service.py
```

Responsibilities

- Compute personalization scores for retrieved memories.
- Rank memories using user interaction history.
- Consider memory importance during retrieval.
- Consider confidence scores during ranking.
- Incorporate access frequency and recency.
- Improve retrieval relevance based on user behavior.

The Personalization Service ensures that search results are tailored to each user by combining retrieval quality with memory importance and interaction history.

---

## 11. Context Retrieval Service

Location

```
backend/app/services/context_retrieval_service.py
```

Responsibilities

- Analyze previous conversation history.
- Resolve follow-up questions.
- Rewrite context-dependent queries.
- Build complete search queries before retrieval.
- Improve conversational memory retrieval.

This service enables the AI assistant to understand references such as pronouns or follow-up questions without requiring the user to repeat previous information.

---

## 12. Diversification Service

Location

```
backend/app/services/diversification_service.py
```

Responsibilities

- Reduce duplicate search results.
- Increase diversity among retrieved memories.
- Improve retrieval quality.
- Ensure a wider range of relevant memories are selected.

The Diversification Service prevents highly similar memories from dominating search results, producing a more balanced context for the language model.

---

## 13. Evaluation Service

Location

```
backend/app/services/evaluation_service.py
```

Responsibilities

- Log every AI request.
- Store retrieval statistics.
- Store response statistics.
- Record retrieval quality metrics.
- Save execution timings.
- Support AI evaluation and analytics dashboards.

The Evaluation Service provides detailed insights into the performance of the Retrieval-Augmented Generation (RAG) pipeline and enables continuous monitoring of AI quality.

---

## 14. Observability Service

Location

```
backend/app/services/observability_service.py
```

Responsibilities

- Measure execution time of each RAG stage.
- Monitor retrieval latency.
- Monitor context selection time.
- Monitor prompt construction time.
- Monitor LLM generation time.
- Record total request execution time.
- Support production performance monitoring.

The Observability Service enables fine-grained performance analysis of the AI pipeline and provides the metrics required for system optimization and production monitoring.

---
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
        ┌───────────────────┼─────────────────────────────┐
        ▼                   ▼                             ▼
Conversation         Context Retrieval            Embedding Service
 History                  Service                        │
        │                   │                            ▼
        │                   ▼                 Sentence Transformer
        │           Query Rewrite Service              │
        │                   │                          │
        └───────────────────┼──────────────────────────┘
                            ▼
                  Hybrid Retrieval Engine
       (Semantic + Keyword + Metadata Search)
                            │
                            ▼
                Cross Encoder Re-ranking
                            │
                            ▼
                 Personalization Service
                            │
                            ▼
                Diversification Service
                            │
                            ▼
               Intelligent Context Selector
                            │
                            ▼
                     Prompt Builder
                            │
                            ▼
                      Google Gemini
                            │
                            ▼
          Evaluation & Observability Services
                            │
                            ▼
                  AI Generated Response
                            │
                            ▼
                  Store Chat Messages
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
- Automatic memory extraction
- Memory classification
- Metadata enrichment
- Sentiment analysis
- Knowledge graph generation
- Hybrid semantic + keyword retrieval
- Query rewriting
- Cross-encoder reranking
- Personalized retrieval
- Context-aware retrieval
- Intelligent context selection
- Duplicate detection
- Long-term memory management
- AI request logging
- Retrieval analytics
- AI observability
- Evaluation dashboards
- Conversation-aware Retrieval-Augmented Generation
- Gemini integration

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

## Summary

The AI subsystem has evolved from a conversational Retrieval-Augmented Generation (RAG) system into a production-grade intelligent memory architecture.

With the completion of **Phase 7**, the assistant now supports:

- Automatic memory understanding and enrichment
- Named entity extraction and metadata generation
- Knowledge graph construction using Neo4j
- Hybrid semantic and keyword retrieval
- Query rewriting and context-aware retrieval
- Cross-encoder AI reranking
- Personalized memory retrieval
- Long-term memory lifecycle management
- Intelligent context selection
- AI observability and performance monitoring
- Retrieval analytics and evaluation dashboards
- Production-style Retrieval-Augmented Generation (RAG)

By combining Sentence Transformers, PostgreSQL, pgvector, Neo4j, Cross Encoder models, Google Gemini, and a modular AI service architecture, the system is capable of delivering highly relevant, context-aware, and personalized responses while continuously monitoring retrieval quality and overall AI performance.

This architecture establishes a scalable foundation for future phases involving document intelligence, multimodal AI, autonomous reasoning, and advanced decision support.