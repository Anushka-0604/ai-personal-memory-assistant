from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.schemas.memory import MemoryCreate, MemoryUpdate

from app.services.archive_service import archive_service
from app.services.classification_service import (
    classification_service,
)
from app.services.cross_encoder_service import (
    cross_encoder_service,
)
from app.services.duplicate_detection_service import (
    duplicate_detection_service,
)
from app.services.embedding_service import (
    generate_embedding,
)
from app.services.extraction_service import (
    ExtractionService,
)
from app.services.graph_builder import GraphBuilder
from app.services.neo4j_service import (
    neo4j_service,
)
from app.services.query_rewrite_service import (
    query_rewrite_service,
)
from app.services.ranking_service import (
    ranking_service,
)
from app.services.sentiment_service import (
    sentiment_service,
)
from app.services.tag_service import (
    tag_service,
)
from app.services.temporal_service import (
    temporal_service,
)

# =====================================================
# Initialize Services
# =====================================================

extraction_service = ExtractionService()

graph_builder = GraphBuilder()

# =====================================================
# Create Memory
# =====================================================

def create_memory(
    db: Session,
    user_id: int,
    memory: MemoryCreate,
):
    # ------------------------------------------
    # Extract structured information
    # ------------------------------------------

    extraction = extraction_service.extract(
        memory.content
    )

    # ------------------------------------------
    # Extract temporal information
    # ------------------------------------------

    temporal_date = temporal_service.extract_date(
        memory.content
    )

    # ------------------------------------------
    # Classify memory
    # ------------------------------------------

    category = classification_service.classify(
        memory.content
    )

    # ------------------------------------------
    # Calculate importance
    # ------------------------------------------

    importance = ranking_service.calculate_importance(
        memory.content
    )

    # ------------------------------------------
    # Generate tags
    # ------------------------------------------

    tags = tag_service.generate_tags(
        extraction
    )

    # ------------------------------------------
    # Analyze sentiment
    # ------------------------------------------

    sentiment, confidence = (
        sentiment_service.analyze(
            memory.content
        )
    )

    # ------------------------------------------
    # Build Knowledge Graph
    # ------------------------------------------

    graph = graph_builder.build(
        extraction
    )

    neo4j_service.save_graph(graph)

    # ------------------------------------------
    # Duplicate Detection
    # ------------------------------------------

    duplicate = (
        duplicate_detection_service.find_duplicate(
            db=db,
            user_id=user_id,
            content=memory.content,
        )
    )

    if duplicate["is_duplicate"]:

        existing_memory = duplicate["memory"]

        # Increase importance
        existing_memory.importance = min(
            (
                existing_memory.importance
                or 0.5
            )
            + 0.05,
            1.0,
        )

        # Increase evidence count
        existing_memory.evidence_count += 1

        # Refresh timestamp
        existing_memory.updated_at = (
            datetime.now(
                timezone.utc
            )
        )

        db.commit()
        db.refresh(existing_memory)

        return existing_memory

    # ------------------------------------------
    # Generate embedding
    # ------------------------------------------

    embedding = generate_embedding(
        memory.content
    )

    # ------------------------------------------
    # Create memory
    # ------------------------------------------

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

# =====================================================
# Get All Memories
# =====================================================

def get_memories(
    db: Session,
    user_id: int,
):
    return (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id
        )
        .all()
    )


# =====================================================
# Get Memory By ID
# =====================================================

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


# =====================================================
# Update Memory
# =====================================================

def update_memory(
    db: Session,
    memory: Memory,
    memory_update: MemoryUpdate,
):
    # ------------------------------------------
    # Update basic fields
    # ------------------------------------------

    memory.content = memory_update.content
    memory.source = memory_update.source

    # ------------------------------------------
    # Extract structured information
    # ------------------------------------------

    extraction = extraction_service.extract(
        memory.content
    )

    # ------------------------------------------
    # Extract temporal information
    # ------------------------------------------

    temporal_date = temporal_service.extract_date(
        memory.content
    )

    # ------------------------------------------
    # Re-classify memory
    # ------------------------------------------

    category = classification_service.classify(
        memory.content
    )

    # ------------------------------------------
    # Recalculate importance
    # ------------------------------------------

    importance = ranking_service.calculate_importance(
        memory.content
    )

    # ------------------------------------------
    # Regenerate tags
    # ------------------------------------------

    tags = tag_service.generate_tags(
        extraction
    )

    # ------------------------------------------
    # Analyze sentiment
    # ------------------------------------------

    sentiment, confidence = (
        sentiment_service.analyze(
            memory.content
        )
    )

    # ------------------------------------------
    # Update Knowledge Graph
    # ------------------------------------------

    graph = graph_builder.build(
        extraction
    )

    neo4j_service.save_graph(graph)

    # ------------------------------------------
    # Regenerate embedding
    # ------------------------------------------

    memory.embedding = generate_embedding(
        memory.content
    )

    # ------------------------------------------
    # Update metadata
    # ------------------------------------------

    memory.extracted_data = (
        extraction.model_dump()
    )

    memory.temporal_date = temporal_date
    memory.category = category
    memory.importance = importance
    memory.tags = tags
    memory.sentiment = sentiment
    memory.confidence = confidence

    db.commit()
    db.refresh(memory)

    return memory


# =====================================================
# Delete Memory
# =====================================================

def delete_memory(
    db: Session,
    memory: Memory,
):
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
    # ------------------------------------------
    # Rewrite the user query
    # ------------------------------------------

    query = query_rewrite_service.rewrite(
        query
    )

    # ------------------------------------------
    # Perform Semantic Search
    # ------------------------------------------

    semantic_results = semantic_search(
        db=db,
        user_id=user_id,
        query=query,
        top_k=top_k,
    )

    # ------------------------------------------
    # Perform Keyword Search
    # ------------------------------------------

    keyword_results = keyword_search(
        db=db,
        user_id=user_id,
        query=query,
        top_k=top_k,
    )

    merged = {}

    # ------------------------------------------
    # Process Semantic Results
    # ------------------------------------------

    for memory, distance in semantic_results:

        similarity = max(
            0.0,
            1 - distance,
        )

        merged[memory.id] = {
            "memory": memory,
            "distance": distance,
            "semantic_score": similarity,
            "keyword_score": 0.0,
        }

    # ------------------------------------------
    # Process Keyword Results
    # ------------------------------------------

    keyword_count = len(
        keyword_results
    )

    for index, memory in enumerate(
        keyword_results
    ):

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
    # Calculate Hybrid Score
    # ------------------------------------------

    results = []

    for item in merged.values():

        hybrid_score = (
            0.7 * item["semantic_score"]
            + 0.3 * item["keyword_score"]
        )

        item["hybrid_score"] = hybrid_score

        results.append(item)
    # ------------------------------------------
    # Keep only the best candidates for reranking
    # ------------------------------------------

    RERANK_TOP_K = max(top_k * 2, 10)

    results.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True,
    )

    results = results[
        : min(RERANK_TOP_K, len(results))
    ]

    # ------------------------------------------
    # Skip CrossEncoder if unnecessary
    # ------------------------------------------

    if len(results) <= 1:

        for item in results:

            item["cross_encoder_score"] = 1.0

            item["retrieval_score"] = item[
                "hybrid_score"
            ]

        return results
    # ------------------------------------------
    # Prepare Memory Texts
    # ------------------------------------------

    memory_texts = [
        item["memory"].content
        for item in results
    ]

    # ------------------------------------------
    # CrossEncoder Re-ranking
    # ------------------------------------------

    cross_scores = cross_encoder_service.rerank(
        query=query,
        memories=memory_texts,
    )

    # ------------------------------------------
    # Normalize CrossEncoder Scores (0 - 1)
    # ------------------------------------------

    if cross_scores:

        min_score = min(cross_scores)
        max_score = max(cross_scores)

        if max_score == min_score:

            normalized_scores = [
                1.0
            ] * len(cross_scores)

        else:

            normalized_scores = [
                (score - min_score)
                / (max_score - min_score)
                for score in cross_scores
            ]

    else:

        normalized_scores = []

    # ------------------------------------------
    # Combine Hybrid + CrossEncoder
    # ------------------------------------------

    for item, cross_score in zip(
        results,
        normalized_scores,
    ):

        item["cross_encoder_score"] = float(
            cross_score
        )

        item["retrieval_score"] = (
            0.6 * item["hybrid_score"]
            + 0.4 * float(cross_score)
        )

    # ------------------------------------------
    # Sort by Retrieval Score
    # ------------------------------------------

    results.sort(
        key=lambda x: x["retrieval_score"],
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
    category: str | None = None,
    sentiment: str | None = None,
    tags: list[str] | None = None,
    start_date=None,
    end_date=None,
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
        cross_encoder_score = item[
            "cross_encoder_score"
        ]
        retrieval_score = item[
            "retrieval_score"
        ]

        # --------------------------------------
        # Metadata Filters
        # --------------------------------------

        if (
            category
            and memory.category != category
        ):
            continue

        if (
            sentiment
            and memory.sentiment != sentiment
        ):
            continue

        if start_date:
            if (
                memory.temporal_date is None
                or memory.temporal_date
                < start_date
            ):
                continue

        if end_date:
            if (
                memory.temporal_date is None
                or memory.temporal_date
                > end_date
            ):
                continue

        if tags:

            memory_tags = memory.tags or []

            if not any(
                tag in memory_tags
                for tag in tags
            ):
                continue

        # --------------------------------------
        # Archive old memories
        # --------------------------------------

        if archive_service.should_archive(
            memory
        ):
            archive_service.archive(memory)
            db.commit()
            continue

        # --------------------------------------
        # Individual Scores
        # --------------------------------------

        similarity_score = max(
            0.0,
            1 - distance,
        )

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

        # --------------------------------------
        # Final Score
        # --------------------------------------

        final_score = (
            ranking_service.calculate_final_score(
                retrieval_score,
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
                "cross_encoder_score": round(
                    cross_encoder_score,
                    4,
                ),
                "retrieval_score": round(
                    retrieval_score,
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