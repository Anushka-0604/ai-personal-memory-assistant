# Database Schema

The AI Personal Memory & Decision Assistant uses **PostgreSQL** as its primary relational database. Vector embeddings are stored using the **pgvector** extension, allowing semantic search directly within PostgreSQL. Neo4j is used alongside PostgreSQL to store the knowledge graph generated from extracted memory entities.

After **Phase 7**, the database contains seven primary tables:

- users
- memories
- chat_sessions
- chat_messages
- user_interactions
- ai_request_logs
- system_metrics

---

# Users Table

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| name | String | User Name |
| email | String | Unique Email Address |
| hashed_password | String | bcrypt Hashed Password |

---

# Memories Table

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id) |
| content | Text | Memory Content |
| source | String | Source of Memory |
| embedding | Vector(384) | Semantic Embedding (pgvector) |
| category | String | Automatically classified memory category |
| importance | Float | Memory importance score |
| tags | JSON / Array | Automatically generated tags |
| sentiment | String | Memory sentiment |
| confidence | Float | Sentiment confidence score |
| temporal_date | Date | Extracted temporal information |
| extracted_data | JSON | Structured extracted entities |
| access_count | Integer | Number of memory accesses |
| last_accessed | Timestamp | Last retrieval timestamp |
| evidence_count | Integer | Number of memory reinforcements |
| is_archived | Boolean | Archive status |
| is_forgotten | Boolean | Forgetting status |
| created_at | Timestamp | Memory Creation Time |
| updated_at | Timestamp | Last Updated Time |

---

# Chat Sessions Table

The **chat_sessions** table stores individual conversations created by users.

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id) |
| title | String | Chat Session Title |
| created_at | Timestamp | Session Creation Time |
| updated_at | Timestamp | Last Activity Time |

---

# Chat Messages Table

The **chat_messages** table stores every message exchanged between the user and the AI assistant.

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| session_id | Integer | Foreign Key (chat_sessions.id) |
| role | String | user / assistant |
| content | Text | Message Content |
| created_at | Timestamp | Message Creation Time |

---

# AI Request Logs Table

The **ai_request_logs** table stores AI evaluation, retrieval, and performance metrics generated during every chat request.

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id) |
| chat_session_id | Integer | Foreign Key (chat_sessions.id) |
| query | Text | User query |
| retrieval_count | Integer | Number of retrieved memories |
| selected_count | Integer | Number of selected memories |
| average_similarity | Float | Average similarity score |
| average_importance | Float | Average importance score |
| average_context_score | Float | Average context score |
| precision_score | Float | Retrieval precision |
| recall_score | Float | Retrieval recall |
| response_generated | Boolean | Whether a response was generated |
| response_length | Integer | Generated response length |
| embedding_time_ms | Float | Embedding generation time |
| retrieval_time_ms | Float | Retrieval execution time |
| ranking_time_ms | Float | Ranking execution time |
| context_time_ms | Float | Context selection time |
| prompt_time_ms | Float | Prompt construction time |
| llm_time_ms | Float | LLM response time |
| total_time_ms | Float | Total request time |
| created_at | Timestamp | Log creation time |

---

# System Metrics Table

The **system_metrics** table stores performance metrics used for monitoring and dashboard generation.

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| metric_name | String | Metric identifier |
| metric_value | Float | Recorded metric value |
| created_at | Timestamp | Metric timestamp |

---

# Entity Relationships

### User → Memory

**Relationship:** One-to-Many

One user can have multiple memories.

Each memory belongs to exactly one user.

---

### User → Chat Session

**Relationship:** One-to-Many

One user can create multiple chat sessions.

Each chat session belongs to exactly one user.

---

### Chat Session → Chat Message

**Relationship:** One-to-Many

One chat session contains multiple chat messages.

Each chat message belongs to exactly one chat session.

---

### User → AI Request Log

**Relationship:** One-to-Many

Each user can generate multiple AI request logs during conversations.

---

### Chat Session → AI Request Log

**Relationship:** One-to-Many

Each chat session can generate multiple AI request logs used for evaluation and analytics.

---

# Current Database Structure

```
PostgreSQL
│
├── users
├── memories
├── chat_sessions
├── chat_messages
├── user_interactions
├── ai_request_logs
└── system_metrics
```

---

# Database Architecture

```
                      Users
                        │
        ┌───────────────┼──────────────────┐
        ▼               ▼                  ▼
    Memories      Chat Sessions     AI Request Logs
        │               │                  │
        │               ▼                  ▼
        │        Chat Messages      System Metrics
        │
        ▼
Vector Embeddings (pgvector)
        │
        ▼
 Knowledge Graph (Neo4j)
```

---

# Conversation Storage Workflow

Whenever the user interacts with the AI assistant, the following process occurs:

1. The user sends a message.
2. Conversation history is retrieved.
3. The query is rewritten using conversation context.
4. Hybrid retrieval is performed using semantic search, keyword search, and metadata filtering.
5. Retrieved memories are reranked using a Cross Encoder.
6. Personalized ranking and intelligent context selection are applied.
7. A prompt is constructed.
8. The Gemini LLM generates a response.
9. User and assistant messages are stored.
10. AI evaluation metrics and execution timings are logged.

This workflow enables accurate, context-aware, and personalized Retrieval-Augmented Generation while continuously monitoring AI performance.

---

# Database Advantages

The current database design provides:

- Secure user management.
- Persistent personal memories.
- Automatic metadata enrichment.
- Knowledge graph integration.
- Semantic search using pgvector.
- Hybrid retrieval support.
- Personalized memory retrieval.
- Long-term memory lifecycle management.
- AI request logging.
- Retrieval analytics.
- System performance monitoring.
- Multi-session conversations.
- Production-grade relational database architecture.

---

# Future Database Expansion

Future phases may introduce additional tables such as:

- uploaded_documents
- document_chunks
- uploaded_images
- voice_memories
- decision_history
- planner_tasks

These additions will support:

- Document Intelligence
- Document Semantic Search
- Multimodal AI
- Voice Intelligence
- Image Understanding
- Decision Support
- Autonomous Planning