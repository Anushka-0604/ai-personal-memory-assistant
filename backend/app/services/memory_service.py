from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.schemas.memory import MemoryCreate, MemoryUpdate
from app.services.classification_service import classification_service
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

def search_memories(
    db: Session,
    user_id: int,
    query: str,
    top_k: int = 5,
):
    query_embedding = generate_embedding(query)

    results = (
        db.query(
            Memory,
            Memory.embedding.cosine_distance(
                query_embedding
            ).label("distance"),
        )
        .filter(Memory.user_id == user_id)
        .order_by(
            Memory.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(top_k)
        .all()
    )

    ranked_results = []

    for memory, distance in results:

        similarity_score = 1 - distance

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

        final_score = (
            similarity_score * 0.6
            + recency_score * 0.2
            + importance_score * 0.2
        )

        ranked_results.append(
            {
                "id": memory.id,
                "content": memory.content,
                "source": memory.source,
                "category": memory.category,
                "importance": memory.importance,
                "tags": memory.tags,
                "sentiment": memory.sentiment,
                "confidence": memory.confidence,
                "access_count": memory.access_count,
                "last_accessed": memory.last_accessed,
                "temporal_date": memory.temporal_date,
                "similarity": round(
                    similarity_score,
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