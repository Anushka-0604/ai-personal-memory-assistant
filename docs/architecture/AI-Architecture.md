# AI Architecture

**Project:** AI Personal Memory & Decision Assistant

**Module:** Artificial Intelligence

**Architecture Version:** v0.5.0

**Last Updated:** After Phase 5

---

# Overview

The Artificial Intelligence layer is responsible for enabling semantic understanding, intelligent retrieval, and AI-powered response generation using the user's stored memories.

Unlike traditional applications that rely on exact keyword matching, the AI layer converts every memory into a dense numerical representation called an **embedding**. These embeddings capture the semantic meaning of the stored information, allowing the application to retrieve memories based on intent and context rather than exact wording.

At the end of Phase 5, the AI subsystem consists of:

- Embedding Generation
- Vector Storage
- Semantic Search
- Retrieval Engine
- Prompt Builder
- Retrieval-Augmented Generation (RAG)
- Gemini LLM Integration

The retrieval engine is now connected to a Large Language Model through a Retrieval-Augmented Generation (RAG) pipeline, enabling the assistant to generate personalized, memory-grounded responses.

Future phases will extend this architecture with conversational memory, automatic memory extraction, context management, and intelligent decision-making.

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

         Top-K Memory Retrieval

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

# AI Pipeline

The AI pipeline transforms human language into intelligent, grounded responses using Retrieval-Augmented Generation.

```
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
- Combine retrieved memories
- Add system instructions
- Include the user's current question

The Prompt Builder ensures that the Large Language Model receives sufficient context to generate grounded and personalized responses.

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

- Perform semantic retrieval
- Filter relevant memories
- Construct prompts
- Invoke the LLM
- Return the final AI response

The Chat Service orchestrates the complete Retrieval-Augmented Generation pipeline.

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

Generated embeddings are stored inside PostgreSQL using the **pgvector** extension.

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

This enables SQL queries to perform semantic similarity search directly inside the database.

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

Whenever a memory is updated:

```
PUT /memories/{id}

↓

Generate New Embedding

↓

Replace Previous Vector
```

This guarantees that stored embeddings always represent the latest version of the memory.

---

# Semantic Search Engine

Instead of performing keyword matching, the AI subsystem performs semantic similarity search.

Workflow

```
User Question

↓

Generate Query Embedding

↓

Cosine Similarity Search

↓

Nearest Embeddings

↓

Top-K Relevant Memories
```

Each retrieved memory is assigned a similarity score, allowing the assistant to identify the most relevant context.

---

# Similarity Metric

Current metric

```
Cosine Similarity
```

Reason

Cosine similarity compares the orientation of vectors instead of their magnitude, making it highly effective for sentence embeddings.

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

Completely unrelated meaning
```

---

# Retrieval-Augmented Generation (RAG)

Phase 5 introduces Retrieval-Augmented Generation.

Instead of generating answers solely from the Large Language Model's pretrained knowledge, the assistant first retrieves relevant memories from the semantic database.

These retrieved memories become the context supplied to the LLM.

Benefits

- Personalized responses
- Reduced hallucinations
- Memory-grounded answers
- Better factual consistency
- Explainable retrieval process

---

# RAG Pipeline

```
User Question

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

↓

Gemini LLM

↓

AI Generated Response
```

---

# Prompt Construction

The Prompt Builder creates structured prompts using:

- System instructions
- Retrieved memories
- User question

Example

```
System:
You are an AI Personal Memory Assistant.

Relevant Memories:
- I have an interview tomorrow at 10 AM.

Question:
What do I have tomorrow?

Answer:
```

Providing structured context helps the LLM generate accurate and grounded responses.

---

# LLM Integration

The assistant currently integrates with:

```
Google Gemini
```

Responsibilities

- Prompt submission
- Response generation
- Error handling
- API abstraction

The rest of the backend remains independent of the chosen LLM provider.

Future LLMs (such as OpenAI or local models) can be integrated with minimal changes.

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

↓

Prompt Builder

↓

Gemini LLM

↓

AI Response
```

---

# Current AI Architecture

```
                 User

                   │

                   ▼

             Chat Service

                   │

         ┌─────────┴─────────┐

         ▼                   ▼

Embedding Service      Prompt Builder

         │                   │

         ▼                   ▼

 Sentence Transformer   Retrieved Memories

         │                   │

         └─────────┬─────────┘

                   ▼

              Gemini LLM

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

## AI Chat

```
Question

↓

Generate Query Embedding

↓

Semantic Search

↓

Retrieved Memories

↓

Prompt Builder

↓

Gemini

↓

AI Response
```
---

# Current Capabilities

The AI subsystem currently supports:

- Automatic embedding generation
- Dense vector representation
- Vector database storage
- Semantic similarity search
- Retrieval of relevant memories
- Retrieval-Augmented Generation (RAG)
- Prompt engineering
- Gemini LLM integration
- AI-generated responses
- Graceful LLM error handling
- Modular AI service architecture

---

# Current Limitations

Although the AI subsystem now supports Retrieval-Augmented Generation, several advanced conversational capabilities are intentionally deferred to future phases.

The current implementation does **not yet support**:

- Short-term conversation history
- Multi-turn dialogue understanding
- Automatic memory extraction
- Session-based conversations
- Context window management
- Memory summarization
- Token optimization

The assistant currently relies exclusively on long-term semantic memory stored in the vector database.

---

# Future AI Roadmap

## Phase 6

Introduce conversational intelligence by implementing:

- Conversation History
- Automatic Memory Extraction
- Session-Based Conversations
- Short-Term Conversational Memory
- Combined Short-Term and Long-Term Memory

---

## Phase 7

Improve context management by adding:

- Context Window Management
- Memory Ranking
- Memory Summarization
- Token Optimization
- Intelligent Context Selection

---

## Phase 8

Introduce intelligent reasoning capabilities:

- Decision Engine
- Personalized Recommendations
- Context-Aware Planning
- Goal Tracking
- Preference Learning

---

## Phase 9

Expand the memory system beyond text:

- Multi-modal Memory
- Image Embeddings
- Document Embeddings
- Voice Memory
- Cross-modal Retrieval

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

This minimizes coupling between components and simplifies maintenance.

---

## Reusability

Core AI services are reusable across multiple backend modules.

For example:

- Embedding generation is used for both memory creation and semantic search.
- Prompt Builder can support multiple LLM providers.
- Chat Service orchestrates the complete RAG workflow.

---

## Scalability

The architecture is designed to support future improvements without major structural changes.

Examples include:

- Replacing the embedding model
- Switching from Gemini to another LLM
- Supporting multiple LLM providers
- Scaling to larger memory collections

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
| Prompt Builder | Construct prompts for the LLM |
| LLM Service | Communicate with Gemini |
| Chat Service | Coordinate the complete RAG pipeline |

This design improves readability, testing, and long-term maintainability.

---

# Summary

The AI subsystem has evolved from a semantic retrieval engine into a complete Retrieval-Augmented Generation (RAG) system.

By combining:

- Sentence Transformers
- PostgreSQL
- pgvector
- Semantic Vector Search
- Prompt Engineering
- Google Gemini

the application can retrieve relevant personal memories and generate grounded, personalized responses.

Phase 5 establishes the foundation for an intelligent AI assistant capable of combining semantic memory retrieval with natural language generation.

Future phases will build upon this foundation by introducing conversational memory, automatic memory extraction, intelligent context management, and decision-making capabilities, ultimately transforming the system into a production-ready AI Personal Memory & Decision Assistant.