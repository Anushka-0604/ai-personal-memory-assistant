# Database Schema

The AI Personal Memory & Decision Assistant uses **PostgreSQL** as its primary relational database. Vector embeddings are stored using the **pgvector** extension, allowing semantic search directly within PostgreSQL. Neo4j is used alongside PostgreSQL to store the knowledge graph generated from extracted memory and document entities.

After **Phase 8**, the database has expanded to support memory intelligence, persistent conversations, document intelligence, document semantic search, retrieval analytics, AI monitoring, and memory-document integration.

The primary PostgreSQL tables include:

* users
* memories
* chat_sessions
* chat_messages
* user_interactions
* ai_request_logs
* system_metrics
* documents
* document_chunks
* retrieval_logs

---

# Users Table

The `users` table stores user account information.

| Column          | Type    | Description            |
| --------------- | ------- | ---------------------- |
| id              | Integer | Primary Key            |
| name            | String  | User Name              |
| email           | String  | Unique Email Address   |
| hashed_password | String  | bcrypt Hashed Password |

---

# Memories Table

The `memories` table stores the user's long-term personal memories together with automatically generated intelligence and metadata.

| Column         | Type         | Description                              |
| -------------- | ------------ | ---------------------------------------- |
| id             | Integer      | Primary Key                              |
| user_id        | Integer      | Foreign Key (`users.id`)                 |
| content        | Text         | Memory Content                           |
| source         | String       | Source of Memory                         |
| embedding      | Vector(384)  | Semantic Embedding (pgvector)            |
| category       | String       | Automatically classified memory category |
| importance     | Float        | Memory importance score                  |
| tags           | JSON / Array | Automatically generated tags             |
| sentiment      | String       | Memory sentiment                         |
| confidence     | Float        | Sentiment confidence score               |
| temporal_date  | Date         | Extracted temporal information           |
| extracted_data | JSON         | Structured extracted entities            |
| access_count   | Integer      | Number of memory accesses                |
| last_accessed  | Timestamp    | Last retrieval timestamp                 |
| evidence_count | Integer      | Number of memory reinforcements          |
| is_archived    | Boolean      | Archive status                           |
| is_forgotten   | Boolean      | Forgetting status                        |
| created_at     | Timestamp    | Memory Creation Time                     |
| updated_at     | Timestamp    | Last Updated Time                        |

---

# Chat Sessions Table

The `chat_sessions` table stores individual conversations created by users.

| Column     | Type      | Description              |
| ---------- | --------- | ------------------------ |
| id         | Integer   | Primary Key              |
| user_id    | Integer   | Foreign Key (`users.id`) |
| title      | String    | Chat Session Title       |
| created_at | Timestamp | Session Creation Time    |
| updated_at | Timestamp | Last Activity Time       |

---

# Chat Messages Table

The `chat_messages` table stores every message exchanged between the user and the AI assistant.

| Column     | Type      | Description                      |
| ---------- | --------- | -------------------------------- |
| id         | Integer   | Primary Key                      |
| session_id | Integer   | Foreign Key (`chat_sessions.id`) |
| role       | String    | user / assistant                 |
| content    | Text      | Message Content                  |
| created_at | Timestamp | Message Creation Time            |

---

# Documents Table

The `documents` table was introduced during Phase 8 to support document intelligence.

It stores uploaded document information, extracted content, and automatically generated document intelligence.

| Column            | Type         | Description                                |
| ----------------- | ------------ | ------------------------------------------ |
| id                | Integer      | Primary Key                                |
| user_id           | Integer      | Foreign Key (`users.id`)                   |
| filename          | String       | Stored document filename                   |
| original_filename | String       | Original uploaded filename                 |
| file_type         | String       | Document file type                         |
| file_size         | Integer      | Document size                              |
| file_path         | String       | Physical storage path                      |
| extracted_text    | Text         | Extracted document content                 |
| document_category | String       | Automatically classified document category |
| keywords          | JSON / Array | Extracted keywords                         |
| entities          | JSON / Array | Extracted named entities                   |
| relationships     | JSON / Array | Extracted entity relationships             |
| created_at        | Timestamp    | Document Creation Time                     |
| updated_at        | Timestamp    | Last Updated Time                          |

### Relationship

```text
One User
   ↓
Many Documents
```

---

# Document Chunks Table

The `document_chunks` table stores smaller semantic units generated from uploaded documents.

These chunks enable efficient semantic document retrieval instead of searching entire documents as a single unit.

| Column      | Type        | Description                       |
| ----------- | ----------- | --------------------------------- |
| id          | Integer     | Primary Key                       |
| document_id | Integer     | Foreign Key (`documents.id`)      |
| chunk_index | Integer     | Position of chunk within document |
| content     | Text        | Chunk Content                     |
| embedding   | Vector(384) | Semantic Embedding (pgvector)     |
| created_at  | Timestamp   | Chunk Creation Time               |

### Relationship

```text
One Document
   ↓
Many Document Chunks
```

---

# AI Request Logs Table

The `ai_request_logs` table stores AI evaluation, retrieval, response, and execution performance metrics generated during chat requests.

| Column                | Type      | Description                      |
| --------------------- | --------- | -------------------------------- |
| id                    | Integer   | Primary Key                      |
| user_id               | Integer   | Foreign Key (`users.id`)         |
| chat_session_id       | Integer   | Foreign Key (`chat_sessions.id`) |
| query                 | Text      | User Query                       |
| retrieval_count       | Integer   | Number of Retrieved Results      |
| selected_count        | Integer   | Number of Selected Results       |
| average_similarity    | Float     | Average Similarity Score         |
| average_importance    | Float     | Average Importance Score         |
| average_context_score | Float     | Average Context Score            |
| precision_score       | Float     | Retrieval Precision              |
| recall_score          | Float     | Retrieval Recall                 |
| response_generated    | Boolean   | Whether a Response Was Generated |
| response_length       | Integer   | Generated Response Length        |
| embedding_time_ms     | Float     | Embedding Generation Time        |
| retrieval_time_ms     | Float     | Retrieval Execution Time         |
| ranking_time_ms       | Float     | Ranking Execution Time           |
| context_time_ms       | Float     | Context Selection Time           |
| prompt_time_ms        | Float     | Prompt Construction Time         |
| llm_time_ms           | Float     | LLM Response Time                |
| total_time_ms         | Float     | Total Request Time               |
| created_at            | Timestamp | Log Creation Time                |

---

# Retrieval Logs Table

The `retrieval_logs` table was introduced during Phase 8 to provide dedicated retrieval analytics.

It records retrieval activity independently so that memory and document retrieval performance can be evaluated.

| Column             | Type      | Description                      |
| ------------------ | --------- | -------------------------------- |
| id                 | Integer   | Primary Key                      |
| user_id            | Integer   | Foreign Key (`users.id`)         |
| chat_session_id    | Integer   | Foreign Key (`chat_sessions.id`) |
| query              | Text      | Retrieval Query                  |
| retrieved_count    | Integer   | Number of Retrieved Results      |
| selected_count     | Integer   | Number of Selected Results       |
| average_similarity | Float     | Average Retrieval Similarity     |
| retrieval_time_ms  | Float     | Retrieval Execution Time         |
| created_at         | Timestamp | Retrieval Log Creation Time      |

### Migration

The table was created through migration:

```text
1f9b08126f2a
```

Description:

```text
add retrieval logs table
```

The migration was successfully applied and verified as the current Alembic head.

---

# System Metrics Table

The `system_metrics` table stores performance metrics used for system monitoring and dashboard generation.

| Column       | Type      | Description           |
| ------------ | --------- | --------------------- |
| id           | Integer   | Primary Key           |
| metric_name  | String    | Metric Identifier     |
| metric_value | Float     | Recorded Metric Value |
| created_at   | Timestamp | Metric Timestamp      |

Phase 8 metrics include:

* Document embedding time
* Document processing time
* Retrieval time
* LLM response time
* Total request time

---

# Entity Relationships

## User → Memory

**Relationship:** One-to-Many

One user can have multiple memories.

Each memory belongs to exactly one user.

---

## User → Chat Session

**Relationship:** One-to-Many

One user can create multiple chat sessions.

Each chat session belongs to exactly one user.

---

## Chat Session → Chat Message

**Relationship:** One-to-Many

One chat session contains multiple chat messages.

Each chat message belongs to exactly one chat session.

---

## User → Document

**Relationship:** One-to-Many

One user can upload multiple documents.

Each document belongs to exactly one user.

---

## Document → Document Chunk

**Relationship:** One-to-Many

One document can contain multiple document chunks.

Each document chunk belongs to exactly one document.

---

## User → AI Request Log

**Relationship:** One-to-Many

Each user can generate multiple AI request logs during conversations.

---

## Chat Session → AI Request Log

**Relationship:** One-to-Many

Each chat session can generate multiple AI request logs used for evaluation and analytics.

---

## User → Retrieval Log

**Relationship:** One-to-Many

Each user can generate multiple retrieval logs during memory and document retrieval.

---

## Chat Session → Retrieval Log

**Relationship:** One-to-Many

Each chat session can generate multiple retrieval logs.

---

## Memory ↔ Document

**Relationship:** Many-to-Many

Memories and documents can be directly associated with each other.

The relationship supports:

```text
Document
   ↕
Memory
```

This allows the system to connect uploaded documents with relevant long-term memories.

---

# Knowledge Graph Relationships

Neo4j stores the knowledge graph separately from PostgreSQL.

The graph represents document entities and relationships:

```text
Document
   │
   ▼
CONTAINS_ENTITY
   │
   ▼
Entity
   │
   ▼
RELATED
   │
   ▼
Entity
```

Cross-document relationships are also supported:

```text
Document A
    │
    ▼
 Entity
    │
    ▼
Relationship
    │
    ▼
 Entity
    │
    ▼
Document B
```

This enables cross-document entity retrieval and multi-hop graph traversal.

---

# Current Database Structure

```text
PostgreSQL
│
├── users
│
├── memories
│
├── chat_sessions
│
├── chat_messages
│
├── user_interactions
│
├── documents
│
├── document_chunks
│
├── ai_request_logs
│
├── retrieval_logs
│
└── system_metrics
```

Alongside PostgreSQL:

```text
Neo4j
│
├── Documents
├── Entities
├── Relationships
└── Cross-Document Connections
```

---

# Database Architecture

```text
                         Users
                           │
        ┌──────────────────┼────────────────────┐
        ▼                  ▼                    ▼
    Memories        Chat Sessions          Documents
        │                  │                    │
        │                  ▼                    ▼
        │            Chat Messages       Document Chunks
        │                                       │
        ▼                                       ▼
 Vector Embeddings                         Vector Embeddings
   (pgvector)                                (pgvector)
        │                                       │
        └───────────────┬───────────────────────┘
                        ▼
               Unified Retrieval
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
    AI Request Logs             Retrieval Logs
          │                           │
          └─────────────┬─────────────┘
                        ▼
                 System Metrics
                        │
                        ▼
                 AI Analytics
```

Knowledge graph:

```text
Documents + Memories
        │
        ▼
      Neo4j
        │
        ▼
Entities
        │
        ▼
Relationships
        │
        ▼
Cross-Document Graph
        │
        ▼
Graph Retrieval
```

---

# Conversation and Retrieval Storage Workflow

Whenever the user interacts with the AI assistant, the following process occurs:

1. The user sends a message.
2. Conversation history is retrieved.
3. The query is rewritten using conversation context.
4. Memory retrieval is performed.
5. Document retrieval is performed when relevant.
6. Retrieved information is combined into a unified context.
7. Retrieved results are reranked and personalized.
8. Intelligent context selection is applied.
9. A prompt is constructed.
10. The Gemini LLM generates a response.
11. User and assistant messages are stored.
12. AI evaluation metrics are logged.
13. Retrieval analytics are recorded.
14. Performance metrics are recorded.

This workflow enables accurate, context-aware, personalized, and document-grounded Retrieval-Augmented Generation while continuously monitoring AI performance.

---

# Document Processing Storage Workflow

Whenever a document is uploaded:

1. The document is stored.
2. Document metadata is created.
3. Text is extracted.
4. The extracted text is stored.
5. The document is classified.
6. Keywords are extracted.
7. Named entities are extracted.
8. Relationships are extracted.
9. The document is divided into chunks.
10. Chunk embeddings are generated.
11. Chunks and embeddings are stored in PostgreSQL/pgvector.
12. Entities and relationships are propagated to Neo4j.
13. The document becomes available for semantic retrieval and document-aware RAG.

---

# Verified Phase 8 Database Statistics

The document dashboard successfully reported:

```text
total_documents = 16

total_chunks = 508

total_storage_bytes = 18126013
```

Retrieval analytics successfully reported:

```text
total_retrievals = 1

average_retrieved = 5

average_selected = 1

average_similarity = 0.3699

average_retrieval_time_ms = 1016.88
```

These results verified that the document and retrieval analytics infrastructure was functioning correctly.

---

# Database Advantages

The current database design provides:

* Secure user management
* Persistent personal memories
* Automatic memory metadata enrichment
* Vector semantic search
* Document storage
* Document chunking
* Document semantic search
* Memory-document integration
* Knowledge graph integration
* Cross-document relationship retrieval
* Hybrid retrieval support
* Personalized memory retrieval
* Long-term memory lifecycle management
* AI request logging
* Retrieval analytics
* Document analytics
* System performance monitoring
* System health monitoring
* Multi-session conversations
* Production-grade relational database architecture

---

# Future Database Expansion

Future phases may introduce additional tables such as:

* uploaded_images
* image_embeddings
* voice_memories
* voice_embeddings
* decision_history
* planner_tasks
* goals
* agent_memory
* multimodal_relationships
* workflow_state

These additions will support:

* Multimodal AI
* Voice Intelligence
* Image Understanding
* Cross-Modal Retrieval
* Decision Support
* Autonomous Planning
* Goal Tracking
* Agentic Workflows

The database architecture will continue to use Alembic for schema version control while maintaining compatibility with the existing PostgreSQL, pgvector, and Neo4j infrastructure.

---

# Summary

With the completion of **Phase 8**, the database has evolved from a memory-focused relational database into a **memory and document intelligence data platform**.

The database now supports:

* User management
* Long-term memory storage
* Memory metadata and lifecycle management
* Persistent conversations
* Vector embeddings
* Document storage
* Document chunks
* Document embeddings
* Semantic document retrieval
* Memory ↔ Document relationships
* AI request logging
* Retrieval logging
* System metrics
* AI analytics
* Knowledge graph storage
* Cross-document relationships
* Performance monitoring
* Health monitoring

The combination of **PostgreSQL, pgvector, and Neo4j** provides the persistent foundation required for semantic memory, document intelligence, conversational RAG, knowledge graph retrieval, and future multimodall AI capabilities.

**PHASE 8 — DATABASE SCHEMA & DOCUMENT INTELLIGENCE: 100% COMPLETE ✅**
