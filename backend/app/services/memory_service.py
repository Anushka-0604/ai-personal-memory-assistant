from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.schemas.memory import MemoryCreate, MemoryUpdate
from app.services.archive_service import archive_service
from app.services.classification_service import classification_service
from app.services.duplicate_detection_service import (
    duplicate_detection_service,
)
from app.services.embedding_service import generate_embedding
from app.services.extraction_service import ExtractionService
from app.services.graph_builder import GraphBuilder
from app.services.neo4j_service import neo4j_service
from app.services.ranking_service import ranking_service
from app.services.sentiment_service import sentiment_service
from app.services.tag_service import tag_service
from app.services.temporal_service import temporal_service

# Initialize the extraction service
extraction_service = ExtractionService()

# Initialize the graph builder
graph_builder = GraphBuilder()


def create_memory(db: Session, user_id: int, memory: MemoryCreate):
    # Extract structured information
    extraction = extraction_service.extract(memory.content)

    # Extract temporal information
    temporal_date = temporal_service.extract_date(
        memory.content
    )

    # Classify memory
    category = classification_service.classify(
        memory.content
    )

    # Calculate importance
    importance = ranking_service.calculate_importance(
        memory.content
    )

    # Generate tags
    tags = tag_service.generate_tags(extraction)

    # Analyze sentiment
    sentiment, confidence = sentiment_service.analyze(
        memory.content
    )

    # Build knowledge graph
    graph = graph_builder.build(extraction)

    # Save graph to Neo4j
    neo4j_service.save_graph(graph)

    # -----------------------------------------------------
    # Duplicate Detection
    # -----------------------------------------------------

    duplicate = duplicate_detection_service.find_duplicate(
        db=db,
        user_id=user_id,
        content=memory.content,
    )

    if duplicate["is_duplicate"]:

        existing_memory = duplicate["memory"]

        # Increase importance slightly
        existing_memory.importance = min(
            (existing_memory.importance or 0.5) + 0.05,
            1.0,
        )

        # Increase evidence count
        existing_memory.evidence_count += 1

        # Refresh timestamp
        existing_memory.updated_at = datetime.now(
            timezone.utc
        )

        db.commit()
        db.refresh(existing_memory)

        return existing_memory

    # Generate vector embedding
    embedding = generate_embedding(memory.content)

    new_memory = Memory(
        user_id=user_id,
        content=memory.content,
        source=memory.source,
        embedding=embedding,
        extracted_data=extraction.model_dump(),
        temporal_date=temporal_date,
        category=category,
        importance=importance,
        tags=tags,
        sentiment=sentiment,
        confidence=confidence,
    )

    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)

    return new_memory


def get_memories(db: Session, user_id: int):
    return (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .all()
    )


def get_memory_by_id(
    db: Session,
    memory_id: int,
    user_id: int,
):
    memory = (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == user_id,
        )
        .first()
    )

    if memory:
        memory.access_count += 1
        memory.last_accessed = datetime.now(
            timezone.utc
        )

        db.commit()
        db.refresh(memory)

    return memory


def update_memory(
    db: Session,
    memory: Memory,
    memory_update: MemoryUpdate,
):
    memory.content = memory_update.content
    memory.source = memory_update.source

    # Re-extract metadata
    extraction = extraction_service.extract(
        memory.content
    )

    # Re-extract temporal information
    temporal_date = temporal_service.extract_date(
        memory.content
    )

    # Re-classify
    category = classification_service.classify(
        memory.content
    )

    # Recalculate importance
    importance = ranking_service.calculate_importance(
        memory.content
    )

    # Regenerate tags
    tags = tag_service.generate_tags(extraction)

    # Recalculate sentiment
    sentiment, confidence = sentiment_service.analyze(
        memory.content
    )

    # Rebuild knowledge graph
    graph = graph_builder.build(extraction)

    # Update graph in Neo4j
    neo4j_service.save_graph(graph)

    # Regenerate embedding
    memory.embedding = generate_embedding(
        memory.content
    )

    # Update metadata
    memory.extracted_data = extraction.model_dump()
    memory.temporal_date = temporal_date
    memory.category = category
    memory.importance = importance
    memory.tags = tags
    memory.sentiment = sentiment
    memory.confidence = confidence

    db.commit()
    db.refresh(memory)

    return memory


def delete_memory(db: Session, memory: Memory):
    db.delete(memory)
    db.commit()

# =====================================================
# Semantic Search
# =====================================================

def semantic_search(
    db: Session,
    user_id: int,
    query: str,
    top_k: int = 5,
):
    query_embedding = generate_embedding(query)

    return (
        db.query(
            Memory,
            Memory.embedding.cosine_distance(
                query_embedding
            ).label("distance"),
        )
        .filter(
            Memory.user_id == user_id,
            Memory.is_archived == False,
        )
        .order_by(
            Memory.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(top_k)
        .all()
    )


# =====================================================
# Keyword Search
# =====================================================

from sqlalchemy import func


def keyword_search(
    db: Session,
    user_id: int,
    query: str,
    top_k: int = 5,
):
    ts_query = func.plainto_tsquery(
        "english",
        query,
    )

    return (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id,
            Memory.is_archived == False,
            func.to_tsvector(
                "english",
                Memory.content,
            ).op("@@")(ts_query),
        )
        .order_by(
            func.ts_rank(
                func.to_tsvector(
                    "english",
                    Memory.content,
                ),
                ts_query,
            ).desc()
        )
        .limit(top_k)
        .all()
    )


# =====================================================
# Hybrid Search
# =====================================================

def hybrid_search(
    db: Session,
    user_id: int,
    query: str,
    top_k: int = 5,
):
    semantic_results = semantic_search(
        db=db,
        user_id=user_id,
        query=query,
        top_k=top_k,
    )

    keyword_results = keyword_search(
        db=db,
        user_id=user_id,
        query=query,
        top_k=top_k,
    )

    merged = {}

    # ------------------------------------------
    # Semantic Results
    # ------------------------------------------

    for memory, distance in semantic_results:

        similarity = max(0.0, 1 - distance)

        merged[memory.id] = {
            "memory": memory,
            "distance": distance,
            "semantic_score": similarity,
            "keyword_score": 0.0,
        }

    # ------------------------------------------
    # Keyword Results
    # ------------------------------------------

    keyword_count = len(keyword_results)

    for index, memory in enumerate(keyword_results):

        # Higher ranked keyword matches receive
        # slightly larger scores.
        keyword_score = (
            (keyword_count - index)
            / max(keyword_count, 1)
        )

        if memory.id in merged:

            merged[memory.id][
                "keyword_score"
            ] = keyword_score

        else:

            merged[memory.id] = {
                "memory": memory,
                "distance": 1.0,
                "semantic_score": 0.0,
                "keyword_score": keyword_score,
            }

    # ------------------------------------------
    # Final Hybrid Score
    # ------------------------------------------

    results = []

    for item in merged.values():

        hybrid_score = (
            0.7 * item["semantic_score"]
            + 0.3 * item["keyword_score"]
        )

        item["hybrid_score"] = hybrid_score

        results.append(item)

    results.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True,
    )

    return results[:top_k]

# =====================================================
# Search Memories
# =====================================================

def search_memories(
    db: Session,
    user_id: int,
    query: str,
    top_k: int = 5,
):
    results = hybrid_search(
        db=db,
        user_id=user_id,
        query=query,
        top_k=top_k,
    )

    ranked_results = []

    for item in results:

        memory = item["memory"]
        distance = item["distance"]
        hybrid_score = item["hybrid_score"]

        if archive_service.should_archive(memory):
            archive_service.archive(memory)
            db.commit()
            continue

        similarity_score = max(0.0, 1 - distance)

        recency_score = (
            ranking_service.calculate_recency_score(
                memory
            )
        )

        importance_score = (
            ranking_service.calculate_importance_score(
                memory
            )
        )

        interaction_score = (
            ranking_service.calculate_interaction_score(
                memory
            )
        )

        # Use hybrid score instead of pure semantic similarity
        final_score = (
            ranking_service.calculate_final_score(
                hybrid_score,
                memory,
            )
        )

        ranked_results.append(
            {
                "id": memory.id,
                "content": memory.content,
                "source": memory.source,
                "category": memory.category,
                "temporal_date": memory.temporal_date,
                "similarity": round(
                    similarity_score,
                    4,
                ),
                "hybrid_score": round(
                    hybrid_score,
                    4,
                ),
                "recency_score": round(
                    recency_score,
                    4,
                ),
                "importance_score": round(
                    importance_score,
                    4,
                ),
                "interaction_score": round(
                    interaction_score,
                    4,
                ),
                "final_score": round(
                    final_score,
                    4,
                ),
            }
        )

    ranked_results.sort(
        key=lambda x: x["final_score"],
        reverse=True,
    )

    return ranked_results