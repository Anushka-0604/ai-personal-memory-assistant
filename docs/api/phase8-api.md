# Phase 8 API Documentation

**Project:** AI Personal Memory & Decision Assistant

**Phase:** Phase 8 – Document Intelligence

**Version:** v0.8.0

---

# Overview

Phase 8 extends the backend APIs by transforming the system from a memory-centric RAG system into a document-aware intelligence system.

The phase introduces document ingestion, text extraction, intelligent document processing, semantic document search, document-aware RAG, knowledge graph integration, memory-document relationships, advanced analytics, performance monitoring, and system health monitoring.

The existing Chat and RAG APIs were enhanced to retrieve and combine information from both user memories and uploaded documents.

---

# Document APIs

## Upload Document

```text
POST /documents/upload
```

### Description

Uploads and processes a document.

During document processing the system automatically performs:

* File Storage
* Text Extraction
* Document Classification
* Keyword Extraction
* Named Entity Recognition
* Relationship Extraction
* Document Chunking
* Embedding Generation
* PostgreSQL/pgvector Storage
* Knowledge Graph Integration

The complete processing pipeline is:

```text
Document Upload
      ↓
File Storage
      ↓
Text Extraction
      ↓
Document Classification
      ↓
Keyword Extraction
      ↓
Entity Extraction
      ↓
Relationship Extraction
      ↓
Document Chunking
      ↓
Embedding Generation
      ↓
PostgreSQL + pgvector
      ↓
Neo4j Knowledge Graph
```

---

# Document Text Extraction

Uploaded document content is extracted using the document extraction service.

The extracted text is stored in:

```text
Document.extracted_text
```

This allows the system to reuse the extracted document content without repeatedly processing the original physical file.

---

# Document Chunking

Document text is divided into smaller semantic chunks.

Each chunk is stored using the `DocumentChunk` model.

Each document chunk contains:

* `id`
* `document_id`
* `chunk_index`
* `content`
* `embedding`
* `created_at`

The document-to-chunk relationship allows large documents to be processed as searchable semantic units.

---

# Document Semantic Search

## Semantic Document Search

```text
POST /documents/search
```

### Description

Performs semantic retrieval over document chunks using embeddings.

The embedding model used is:

```text
all-MiniLM-L6-v2
```

Embedding dimension:

```text
384
```

Embeddings are stored using:

```text
pgvector
```

The retrieval process performs:

1. Generate query embedding
2. Compare against document chunk embeddings
3. Calculate cosine distance
4. Convert distance into similarity
5. Rank results
6. Remove duplicate chunks
7. Return Top-K results
8. Optionally group results by document

Supported search filters include:

* `document_id`
* `file_type`
* `upload_date`
* `top_k`
* `group_by_document`

Duplicate chunks are identified using document filename and chunk content to prevent repeated content from occupying multiple retrieval positions.

---

# Document-Aware Chat API

## Chat

```text
POST /chat
```

### Description

The Chat API was enhanced to support both memories and documents.

The updated conversational pipeline performs:

1. Retrieve conversation history
2. Resolve references
3. Generate conversation-aware search query
4. Retrieve relevant memories
5. Retrieve relevant document chunks
6. Select unified context
7. Construct prompt
8. Generate Gemini response
9. Record analytics
10. Store chat messages

The updated pipeline is:

```text
Question
   ↓
Conversation Context
   ↓
Reference Resolution
   ↓
Conversation-Aware Search
   ↓
Memory Retrieval
   +
Document Retrieval
   ↓
Context Selection
   ↓
Unified Context
   ↓
Prompt Builder
   ↓
Gemini LLM
   ↓
AI Response
```

The prompt explicitly instructs the LLM to use both memory content and document excerpts when relevant.

---

# Document Intelligence

Documents are automatically enriched with metadata.

The Document model contains:

| Field             | Description                       |
| ----------------- | --------------------------------- |
| filename          | Stored document filename          |
| original_filename | Original uploaded filename        |
| file_type         | Document file type                |
| file_size         | File size                         |
| file_path         | Storage path                      |
| extracted_text    | Extracted document content        |
| document_category | Automatically classified category |
| keywords          | Extracted keywords                |
| entities          | Extracted named entities          |
| relationships     | Extracted relationships           |
| created_at        | Creation timestamp                |
| updated_at        | Last update timestamp             |

The document processing pipeline performs:

```text
Text Extraction
      ↓
Classification
      ↓
Keyword Extraction
      ↓
NER
      ↓
Relationship Extraction
      ↓
Database Storage
```

---

# Memory ↔ Document APIs

Phase 8 introduces direct relationships between memories and documents.

The system supports:

```text
Document → Memories
Memory → Documents
```

## Link Memory to Document

```text
POST /documents/{document_id}/memories/{memory_id}
```

Creates a relationship between a document and a memory.

---

## Get Document Memories

```text
GET /documents/{document_id}/memories
```

Returns memories associated with a document.

---

## Get Memory Documents

```text
GET /memories/{memory_id}/documents
```

Returns documents associated with a memory.

All memory-document APIs verify that the requested resources belong to the authenticated user.

---

# Knowledge Graph APIs

Neo4j was integrated as the knowledge graph layer for document intelligence.

The graph represents:

```text
Document
   ↓
CONTAINS_ENTITY
   ↓
Entity
   ↓
RELATED
   ↓
Entity
```

Documents, entities, and relationships extracted during document processing are propagated into Neo4j.

---

# Graph Query APIs

## Get People

```text
GET /graph/people
```

Returns people represented in the knowledge graph.

---

## Get Organizations

```text
GET /graph/organizations
```

Returns organizations represented in the knowledge graph.

---

## Get Locations

```text
GET /graph/locations
```

Returns locations represented in the knowledge graph.

---

## Get Document Entities

```text
GET /graph/document/{document_id}/entities
```

Returns entities associated with a document.

---

## Get Document Relationships

```text
GET /graph/document/{document_id}/relationships
```

Returns relationships associated with a document.

---

## Get Entity Connections

```text
GET /graph/entity/{entity_name}/connections
```

Returns entities connected to the specified entity.

---

## Person → Organizations

```text
GET /graph/person/{person_name}/organizations
```

Returns organizations associated with a person.

---

## Organization → People

```text
GET /graph/organization/{organization_name}/people
```

Returns people associated with an organization.

---

## Person → Locations

```text
GET /graph/person/{person_name}/locations
```

Returns locations associated with a person.

---

## Location → People

```text
GET /graph/location/{location_name}/people
```

Returns people associated with a location.

---

## Organization → Locations

```text
GET /graph/organization/{organization_name}/locations
```

Returns locations associated with an organization.

---

## Location → Organizations

```text
GET /graph/location/{location_name}/organizations
```

Returns organizations associated with a location.

---

## Entity → Documents

```text
GET /graph/entity/{entity_name}/documents
```

Returns documents containing the specified entity.

---

# Cross-Document Relationships

## Cross-Document Entity Relationships

```text
GET /graph/entity/{entity_name}/cross-document
```

### Description

Identifies relationships involving an entity across multiple documents.

The API can answer questions such as:

* Where does this entity appear across documents?
* What relationships involving this entity exist across different documents?

The implementation uses:

```text
get_cross_document_relationships()
```

---

# Graph Retrieval

Phase 8 introduces graph-based retrieval capabilities.

Implemented retrieval operations include:

* Entity → Documents
* Memory → Documents
* Document → Memories
* Multi-hop Entity Traversal
* Cross-Document Relationship Retrieval

Implemented methods include:

```text
get_documents_for_entity()

get_documents_for_memory()

get_memories_for_document()

get_entity_connections_by_depth()

get_cross_document_relationships()
```

Multi-hop traversal supports a configurable depth between:

```text
1 and 5
```

This restriction prevents excessively large graph traversals.

### Verified Graph Retrieval

The entity:

```text
CPU
```

was tested successfully.

The graph returned:

```text
document_13 → 1_Introduction.pdf
document_12 → 2_Process_Management.pdf
document_14 → 2_Process_Management.pdf
```

Therefore:

```text
ENTITY → DOCUMENT GRAPH RETRIEVAL = VERIFIED
```

---

# Analytics APIs

Phase 8 introduces advanced document, usage, retrieval, performance, and health analytics.

---

## Document Dashboard

```text
GET /analytics/document-dashboard
```

Returns:

* Total documents
* Total chunks
* Total storage

Verified result:

```text
total_documents = 16
total_chunks = 508
total_storage_bytes = 18126013
```

---

## Usage Dashboard

```text
GET /analytics/usage-dashboard
```

Returns:

* Total requests
* Successful requests
* Failed requests
* Average response time
* Average similarity
* Average response length

Usage analytics are generated from AI request logs.

---

## Retrieval Analytics

```text
GET /analytics/retrieval-analytics
```

Tracks:

* Total retrievals
* Average retrieved results
* Average selected results
* Average similarity
* Retrieval time

Retrieval logs store:

| Field              | Description                  |
| ------------------ | ---------------------------- |
| user_id            | User performing the request  |
| chat_session_id    | Associated chat session      |
| query              | Search query                 |
| retrieved_count    | Number of retrieved results  |
| selected_count     | Number of selected results   |
| average_similarity | Average retrieval similarity |
| retrieval_time_ms  | Retrieval execution time     |
| created_at         | Timestamp                    |

Verified result:

```text
total_retrievals = 1
average_retrieved = 5
average_selected = 1
average_similarity = 0.3699
average_retrieval_time_ms = 1016.88
```

---

# Performance Monitoring

## System Metrics

```text
GET /analytics/system-metrics
```

Tracks major stages of the AI pipeline.

Metrics include:

* LLM response time
* Retrieval time
* Total request time
* Document processing time
* Document embedding time

The `SystemMetric` model stores:

| Field        | Description                |
| ------------ | -------------------------- |
| id           | Metric identifier          |
| metric_name  | Name of performance metric |
| metric_value | Recorded value             |
| unit         | Metric unit                |
| created_at   | Timestamp                  |

Verified metrics included:

```text
document_embedding_time
≈ 5919.22 ms

document_processing_time
≈ 7233.51 ms

total_request_time
≈ 23049.56 ms

retrieval_time
≈ 1016.88 ms

llm_response_time
≈ 21972.64 ms
```

---

# System Health

## Health Check

```text
GET /system/health
```

Checks:

1. Database
2. Embedding model
3. LLM service
4. CPU
5. Memory
6. Disk

Database health is verified using:

```sql
SELECT 1
```

Embedding model health is checked through the loaded model.

LLM health is checked through `LLMService`.

System resources are measured using:

```text
psutil
```

Disk usage is calculated using:

```text
shutil.disk_usage()
```

Verified response included:

```text
database:
Healthy

embedding_model:
Healthy

llm_service:
Healthy

cpu_percent:
26.5

memory_percent:
92.7

disk_percent:
20.64
```

All health components successfully responded.

---

# AI Dashboard

## AI Dashboard

```text
GET /analytics/ai-dashboard
```

Provides a unified view of:

* Retrieval Quality
* Usage Statistics
* System Health
* Performance Metrics

Verified retrieval statistics included:

```text
average_similarity = 0.3699
average_selected = 1
average_retrieved = 5
average_response_length = 426
response_rate = 100
```

Usage statistics included:

```text
total_requests = 1
successful_requests = 1
failed_requests = 0
average_response_time_ms = 23049.56
average_similarity = 0.3699
average_response_length = 426
```

System metric statistics included:

```text
total_metrics = 3
average_metric_value = 15346.36
latest_metric = total_request_time
```

---

# Chat and Analytics Debugging

Several integration issues were identified and resolved during Phase 8 testing.

## Missing Retrieval Logs Table

The retrieval analytics endpoint initially returned:

```text
500 Internal Server Error
```

because the:

```text
retrieval_logs
```

table did not exist.

### Resolution

The issue was fixed by:

1. Updating Alembic model imports
2. Generating a database migration
3. Creating the `retrieval_logs` migration
4. Applying the migration using:

```text
alembic upgrade head
```

Migration:

```text
1f9b08126f2a
```

After migration, retrieval analytics worked successfully.

---

## Missing Chat Session

A `/chat` request initially failed because:

```text
session_id = 1
```

did not exist in `chat_sessions`.

PostgreSQL rejected the request because `chat_messages.session_id` has a foreign-key relationship with `chat_sessions.id`.

The issue was resolved by creating or using a valid chat session before sending the chat request.

---

## Document Search Return Format

The ChatService initially expected document search results in the form:

```text
chunk, distance
```

However, `semantic_document_search()` had been updated to return `DocumentSearchResult` objects.

This caused:

```text
ValueError:
too many values to unpack (expected 2)
```

The ChatService was updated to work with the new `DocumentSearchResult` structure.

---

# Successful Document RAG Verification

After resolving the integration issues, the `/chat` endpoint successfully returned:

```text
HTTP 200
```

The query:

```text
"What is CPU?"
```

successfully retrieved both:

* Memory context
* Document context

The final prompt contained document excerpts related to:

* CPU
* Operating Systems
* Computer System Components
* Process State
* User Mode
* CPU Registers

Gemini successfully generated the final response.

Measured performance:

```text
Retrieval:
≈ 1016.88 ms

LLM:
≈ 21972.64 ms

Total:
≈ 23049.56 ms
```

The successful request also generated analytics data used by the Usage, Retrieval Analytics, and Performance Monitoring modules.

---

# Database and Alembic Changes

Phase 8 introduced the retrieval logging database infrastructure.

Migration:

```text
1f9b08126f2a
```

Description:

```text
add retrieval logs table
```

Migration chain:

```text
4a6ad9123071
        ↓
1f9b08126f2a
```

Verified using:

```text
alembic current
```

Result:

```text
1f9b08126f2a (head)
```

And:

```text
alembic heads
```

Result:

```text
1f9b08126f2a (head)
```

The migration was successfully applied using:

```text
alembic upgrade head
```

---

# Important Components

### Document Components

* `document.py`
* `document_chunk.py`
* `document_service.py`
* `document_extraction_service.py`
* `document_chunking_service.py`
* `document_search_service.py`
* `document_dashboard_service.py`
* `document_usage_service.py`

### Document Intelligence

* `classification_service.py`
* `keyword_extraction_service.py`
* `ner_service.py`
* `relationship_extraction_service.py`
* `embedding_service.py`

### Knowledge Graph

* `neo4j_service.py`
* `graph_query_service.py`
* Graph Query APIs

### Memory Integration

* `memory_document_service.py`

### Analytics

* `usage_dashboard_service.py`
* `retrieval_analytics_service.py`
* `retrieval_quality_service.py`
* `system_metric_service.py`
* `health_service.py`
* `ai_dashboard_service.py`

### Database Models

* `Document`
* `DocumentChunk`
* `RetrievalLog`
* `SystemMetric`

### Schemas

* `DocumentDashboard`
* `DocumentUsageStatistics`
* `UsageDashboard`
* `RetrievalAnalyticsResponse`
* `RetrievalQualityResponse`
* `AIDashboardResponse`

---

# Phase 8 API Improvements

Compared to Phase 7, the APIs now support:

* Document ingestion
* Automatic text extraction
* Document chunking
* Document embeddings
* Semantic document search
* Document-aware RAG
* Unified memory + document retrieval
* Document classification
* Keyword extraction
* Named Entity Recognition
* Relationship extraction
* Neo4j knowledge graph integration
* Cross-document relationships
* Graph query APIs
* Multi-hop graph retrieval
* Memory ↔ Document relationships
* Document analytics
* Retrieval analytics
* Usage analytics
* Performance monitoring
* System health monitoring
* Unified AI dashboard

---

# Final Phase 8 Architecture

The completed document intelligence pipeline is:

```text
USER
  ↓
Authentication
  ↓
Document Upload
  ↓
File Storage
  ↓
Text Extraction
  ↓
Document Classification
  ↓
Keyword Extraction
  ↓
NER
  ↓
Relationship Extraction
  ↓
Document Chunking
  ↓
Embedding Generation
  ↓
PostgreSQL + pgvector
  ↓
Semantic Retrieval
  ↓
Memory Retrieval
  ↓
Unified RAG Context
  ↓
Gemini LLM
  ↓
AI Response
  ↓
Analytics + Evaluation
  ↓
Performance Monitoring
  ↓
Health Monitoring
```

Knowledge graph pipeline:

```text
Document
  ↓
Neo4j
  ↓
Entities
  ↓
Relationships
  ↓
Cross-Document Graph Queries
  ↓
Graph Retrieval
```

Integrated relationship:

```text
Memory
   ↔
Document
   ↔
Knowledge Graph
```

---

# Phase 8 Final Status

| Module                                | Status |
| ------------------------------------- | ------ |
| Document Ingestion                    | ✅      |
| Document Extraction                   | ✅      |
| Document Chunking                     | ✅      |
| Embeddings & Semantic Search          | ✅      |
| Document RAG / Chat                   | ✅      |
| Document Intelligence                 | ✅      |
| Memory ↔ Document Integration         | ✅      |
| Knowledge Graph Foundation            | ✅      |
| F1 — Neo4j Integration                | ✅      |
| F2 — Entity & Relationship Extraction | ✅      |
| F3 — Cross-Document Relationships     | ✅      |
| F4 — Graph Query APIs                 | ✅      |
| F5 — Graph Retrieval                  | ✅      |
| G1 — Document Dashboard               | ✅      |
| G2 — Usage Analytics                  | ✅      |
| G3 — Retrieval Analytics              | ✅      |
| G4 — Performance Monitoring           | ✅      |
| G5 — Health Metrics                   | ✅      |

---

# Summary

Phase 8 significantly expands the AI Personal Memory & Decision Assistant from a memory-centric RAG system into a complete document-aware intelligence platform.

The APIs now support document ingestion, intelligent document processing, semantic search, document-aware RAG, unified memory and document retrieval, knowledge graph reasoning, cross-document relationships, graph retrieval, memory-document relationships, analytics, performance monitoring, and system health monitoring.

All Phase 8 modules, including the remaining F5 and G5 tasks, were implemented, integrated, tested, and verified.

**PHASE 8 — DOCUMENT INTELLIGENCE: 100% COMPLETE ohh ✅**
