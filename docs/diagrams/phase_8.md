# Phase 8 — System Diagrams

**Project:** AI Personal Memory & Decision Assistant

**Phase:** Phase 8 – Document Intelligence

**Status:** 100% Complete ✅

---

# 1. Phase 8 Overall Architecture

The Phase 8 architecture extends the existing memory-based AI system by introducing document intelligence, document semantic search, knowledge graph integration, and unified memory + document RAG.

```text
                                USER
                                  │
                                  ▼
                           FastAPI Backend
                                  │
             ┌────────────────────┼─────────────────────┐
             ▼                    ▼                     ▼
      Authentication       Memory Services       Document Services
             │                    │                     │
             ▼                    ▼                     ▼
       JWT Verification   Memory Intelligence    Document Upload
                                  │                     │
                                  ▼                     ▼
                         Embedding Service       File Storage
                                  │                     │
                                  │                     ▼
                                  │              Text Extraction
                                  │                     │
                                  │                     ▼
                                  │          Document Intelligence
                                  │              ┌──────┼──────┐
                                  │              ▼      ▼      ▼
                                  │        Classification Keywords NER
                                  │                     │
                                  │                     ▼
                                  │            Relationship Extraction
                                  │                     │
                                  │                     ▼
                                  │              Document Chunking
                                  │                     │
                                  │                     ▼
                                  │              Document Embeddings
                                  │                     │
                                  └──────────┬──────────┘
                                             ▼
                                  PostgreSQL + pgvector
                                             │
                                             ▼
                                  Unified Retrieval Layer
                                             │
                                             ▼
                                  Cross Encoder Re-ranking
                                             │
                                             ▼
                                    Personalization
                                             │
                                             ▼
                                    Diversification
                                             │
                                             ▼
                                  Context Selection
                                             │
                                             ▼
                                      Prompt Builder
                                             │
                                             ▼
                                      Google Gemini
                                             │
                                             ▼
                                    AI Response
                                             │
                                             ▼
                               Analytics & Monitoring
```

---

# 2. Phase 8 Document Processing Pipeline

This diagram represents the complete document ingestion and processing workflow.

```text
User Uploads Document
        │
        ▼
Document Upload API
        │
        ▼
File Storage
        │
        ▼
Text Extraction
        │
        ▼
Document Classification
        │
        ▼
Keyword Extraction
        │
        ▼
Named Entity Recognition
        │
        ▼
Relationship Extraction
        │
        ▼
Document Chunking
        │
        ▼
Generate Embeddings
        │
        ▼
PostgreSQL + pgvector
        │
        ▼
Document Available
for Semantic Retrieval
```

---

# 3. Document Intelligence Pipeline

Phase 8 enriches uploaded documents with structured intelligence.

```text
                    DOCUMENT
                        │
                        ▼
                  Extract Text
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
        Classification Keywords     NER
             │          │          │
             └──────────┼──────────┘
                        ▼
              Relationship Extraction
                        │
                        ▼
                Structured Metadata
                        │
                        ▼
                  Document Chunks
                        │
                        ▼
                    Embeddings
                        │
                        ▼
                 Vector Database
```

---

# 4. Document Chunking Diagram

Large documents are divided into smaller semantic units before embeddings are generated.

```text
                    DOCUMENT
                        │
                        ▼
                  Extracted Text
                        │
                        ▼
                 Chunking Service
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
         Chunk 1     Chunk 2     Chunk 3
            │           │           │
            ▼           ▼           ▼
        Embedding   Embedding   Embedding
            │           │           │
            └───────────┼───────────┘
                        ▼
                  pgvector
```

Each chunk contains:

```text
Document ID
Chunk Index
Content
Embedding
Created At
```

---

# 5. Memory + Document Unified Retrieval

Phase 8 introduces unified retrieval across two sources of knowledge.

```text
                         USER QUERY
                              │
                              ▼
                       Query Embedding
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
        MEMORY RETRIEVAL             DOCUMENT RETRIEVAL
                │                           │
                ▼                           ▼
        Memory Embeddings           Document Embeddings
                │                           │
                └─────────────┬─────────────┘
                              ▼
                     Unified Retrieval
                              │
                              ▼
                    Cross Encoder Ranking
                              │
                              ▼
                       Personalization
                              │
                              ▼
                       Diversification
                              │
                              ▼
                     Context Selection
                              │
                              ▼
                       Prompt Builder
                              │
                              ▼
                          Gemini
                              │
                              ▼
                       AI Response
```

---

# 6. Document Semantic Search

The document semantic search process is:

```text
User Query
    │
    ▼
Generate Query Embedding
    │
    ▼
Compare with Document Chunk Embeddings
    │
    ▼
Cosine Distance
    │
    ▼
Convert Distance → Similarity
    │
    ▼
Rank Results
    │
    ▼
Remove Duplicate Chunks
    │
    ▼
Top-K Results
    │
    ▼
Optional Document Grouping
```

Supported filters:

```text
Document ID
File Type
Upload Date
Top-K
Group By Document
```

---

# 7. Knowledge Graph Architecture

Phase 8 integrates document intelligence with Neo4j.

```text
                    DOCUMENT
                        │
                        ▼
                      Neo4j
                        │
                        ▼
                     ENTITY
                        │
                  ┌─────┴─────┐
                  ▼           ▼
              ENTITY       ENTITY
                  │           │
                  └─────┬─────┘
                        ▼
                   RELATIONSHIP
```

Basic graph structure:

```text
Document
   │
   └── CONTAINS_ENTITY ──► Entity
                              │
                              └── RELATED ──► Entity
```

---

# 8. Cross-Document Relationship Diagram

Phase 8 supports relationships between entities appearing in multiple documents.

```text
             DOCUMENT A
                  │
                  ▼
              ENTITY X
                  │
             RELATED TO
                  │
                  ▼
              ENTITY Y
                  ▲
                  │
             FOUND IN
                  │
                  │
             DOCUMENT B
```

More generally:

```text
Document A
    │
    ▼
Entity A
    │
    ▼
Relationship
    │
    ▼
Entity B
    │
    ▼
Document B
```

This enables the system to identify where an entity appears across multiple documents and what relationships exist across those documents.

---

# 9. Multi-Hop Graph Retrieval

Graph traversal supports configurable depths from 1 to 5.

```text
Entity
  │
  ▼
Depth 1
  │
  ▼
Connected Entity
  │
  ▼
Depth 2
  │
  ▼
Connected Entity
  │
  ▼
Depth 3
  │
  ▼
Connected Entity
  │
  ▼
Depth 4
  │
  ▼
Connected Entity
  │
  ▼
Depth 5
```

The depth limit prevents excessively large graph traversals.

---

# 10. Memory ↔ Document Integration

Phase 8 creates a direct relationship between memories and uploaded documents.

```text
                    MEMORY
                       │
                       ↕
                MEMORY-DOCUMENT
                  RELATIONSHIP
                       ↕
                    DOCUMENT
```

Supported operations:

```text
Document → Memories

Memory → Documents
```

This allows the assistant to connect personal memories with supporting documents.

---

# 11. Complete RAG Pipeline

The Phase 8 RAG pipeline combines conversation context, memories, documents, and AI generation.

```text
USER QUESTION
      │
      ▼
Conversation History
      │
      ▼
Reference Resolution
      │
      ▼
Query Rewrite
      │
      ▼
Generate Query Embedding
      │
      ├───────────────────┐
      ▼                   ▼
Memory Search       Document Search
      │                   │
      └─────────┬─────────┘
                ▼
         Unified Retrieval
                │
                ▼
       Cross Encoder Ranking
                │
                ▼
         Personalization
                │
                ▼
         Diversification
                │
                ▼
        Context Selection
                │
                ▼
          Prompt Builder
                │
                ▼
            Gemini LLM
                │
                ▼
          AI Response
                │
                ▼
      Evaluation & Analytics
```

---

# 12. Analytics Architecture

Phase 8 introduced advanced analytics for documents, retrieval, usage, and system performance.

```text
                         AI REQUEST
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
       Retrieval Logs    AI Request Logs   System Metrics
              │               │                │
              ▼               ▼                ▼
       Retrieval Data    Usage Data      Performance Data
              │               │                │
              └───────────────┼────────────────┘
                              ▼
                       AI Dashboard
```

---

# 13. Document Analytics

The document dashboard tracks:

```text
Documents
   │
   ├── Total Documents
   │
   ├── Total Chunks
   │
   └── Total Storage
```

Verified Phase 8 values:

```text
total_documents = 16

total_chunks = 508

total_storage_bytes = 18126013
```

---

# 14. Retrieval Analytics

```text
Retrieval Request
       │
       ▼
RetrievalLog
       │
       ├── Query
       ├── Retrieved Count
       ├── Selected Count
       ├── Average Similarity
       └── Retrieval Time
       │
       ▼
Retrieval Analytics
```

Verified values:

```text
total_retrievals = 1

average_retrieved = 5

average_selected = 1

average_similarity = 0.3699

average_retrieval_time_ms = 1016.88
```

---

# 15. Performance Monitoring

Phase 8 tracks the major execution stages of the AI pipeline.

```text
AI Request
    │
    ├── Document Processing
    │
    ├── Document Embedding
    │
    ├── Retrieval
    │
    ├── LLM Generation
    │
    └── Total Request
             │
             ▼
       System Metrics
```

Verified metrics:

```text
document_embedding_time
≈ 5919.22 ms

document_processing_time
≈ 7233.51 ms

retrieval_time
≈ 1016.88 ms

llm_response_time
≈ 21972.64 ms

total_request_time
≈ 23049.56 ms
```

---

# 16. System Health Architecture

```text
                     Health Service
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
      Database        Embedding Model    LLM Service
          │                │                │
          └────────────────┼────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
         CPU             Memory            Disk
                           │
                           ▼
                     Health Response
```

Verified health status:

```text
database = Healthy

embedding_model = Healthy

llm_service = Healthy

cpu_percent = 26.5

memory_percent = 92.7

disk_percent = 20.64
```

---

# 17. AI Dashboard Architecture

The AI dashboard combines multiple monitoring layers.

```text
                 AI Dashboard Service
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
Retrieval Quality   Usage Analytics   System Health
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                Unified AI Dashboard
```

Verified dashboard information includes:

```text
average_similarity = 0.3699
average_selected = 1
average_retrieved = 5
average_response_length = 426
response_rate = 100

total_requests = 1
successful_requests = 1
failed_requests = 0
average_response_time_ms = 23049.56
```

---

# 18. Complete Phase 8 Architecture

The complete Phase 8 architecture combines all major subsystems.

```text
                              USER
                                │
                                ▼
                         FastAPI Backend
                                │
        ┌───────────────────────┼─────────────────────────┐
        ▼                       ▼                         ▼
 Authentication           Memory System             Document System
        │                       │                         │
        ▼                       ▼                         ▼
      JWT                 Memory Intelligence       Document Upload
                                │                         │
                                ▼                         ▼
                         Memory Embeddings         Text Extraction
                                │                         │
                                │                         ▼
                                │                 Document Intelligence
                                │                         │
                                │                         ▼
                                │                 Document Chunking
                                │                         │
                                │                         ▼
                                │                 Document Embeddings
                                │                         │
                                └───────────┬─────────────┘
                                            ▼
                                   PostgreSQL + pgvector
                                            │
                                            ▼
                                   Unified Retrieval
                                            │
                              ┌─────────────┴─────────────┐
                              ▼                           ▼
                        Memory Search              Document Search
                              │                           │
                              └─────────────┬─────────────┘
                                            ▼
                                   Cross Encoder
                                            │
                                            ▼
                                    Personalization
                                            │
                                            ▼
                                    Diversification
                                            │
                                            ▼
                                  Context Selection
                                            │
                                            ▼
                                      Prompt Builder
                                            │
                                            ▼
                                      Google Gemini
                                            │
                                            ▼
                                      AI Response
                                            │
                      ┌─────────────────────┼─────────────────────┐
                      ▼                     ▼                     ▼
                 Retrieval             Performance            Health
                 Analytics             Monitoring            Monitoring
                      │                     │                     │
                      └─────────────────────┼─────────────────────┘
                                            ▼
                                      AI Dashboard


                         DOCUMENT KNOWLEDGE GRAPH
                                      │
                                      ▼
                                    Neo4j
                                      │
                                      ▼
                          Entities + Relationships
                                      │
                                      ▼
                         Cross-Document Retrieval
                                      │
                                      ▼
                              Graph Query APIs
```

---

# 19. Phase 8 Data Flow

```text
                         DATA INGESTION
                              │
          ┌───────────────────┴───────────────────┐
          ▼                                       ▼
       Memory                                  Document
          │                                       │
          ▼                                       ▼
   Memory Intelligence                    Text Extraction
          │                                       │
          ▼                                       ▼
      Embedding                            Document Intelligence
          │                                       │
          │                                       ▼
          │                                  Chunking
          │                                       │
          │                                       ▼
          │                                   Embedding
          │                                       │
          └───────────────────┬───────────────────┘
                              ▼
                       Vector Database
                              │
                              ▼
                       Semantic Retrieval
                              │
                              ▼
                    Unified RAG Context
                              │
                              ▼
                         Gemini LLM
                              │
                              ▼
                         AI Response
                              │
                              ▼
                   Analytics + Monitoring
```

---

# 20. Phase 8 Final Architecture Summary

Phase 8 transforms the system from a memory-centric RAG application into a **document-aware AI intelligence platform**.

The final architecture consists of:

```text
Memory Intelligence
        +
Document Intelligence
        +
Vector Retrieval
        +
Knowledge Graph
        +
Conversational RAG
        +
Analytics
        +
Performance Monitoring
        +
Health Monitoring
        │
        ▼
AI Personal Memory & Decision Assistant
```

The core Phase 8 relationship is:

```text
                    MEMORY
                       │
                       │
                       ▼
                 VECTOR SEARCH
                       ▲
                       │
                       │
                  DOCUMENT
                       │
                       ▼
                KNOWLEDGE GRAPH
                       │
                       ▼
              GRAPH RETRIEVAL
                       │
                       ▼
                UNIFIED CONTEXT
                       │
                       ▼
                  GEMINI LLM
                       │
                       ▼
                  AI RESPONSE
```

**PHASE 8 — DOCUMENT INTELLIGENCE DIAGRAMS: 100% COMPLETE ✅**
