from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.schemas.memory import MemoryCreate, MemoryUpdate
from app.services.embedding_service import generate_embedding
from app.services.extraction_service import ExtractionService
from app.services.graph_builder import GraphBuilder
from app.services.neo4j_service import neo4j_service

# Initialize the extraction service
extraction_service = ExtractionService()

# Initialize the graph builder
graph_builder = GraphBuilder()


def create_memory(db: Session, user_id: int, memory: MemoryCreate):
    # Extract structured information from the memory
    extraction = extraction_service.extract(memory.content)

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


def get_memory_by_id(db: Session, memory_id: int, user_id: int):
    return (
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == user_id,
        )
        .first()
    )


def update_memory(
    db: Session,
    memory: Memory,
    memory_update: MemoryUpdate,
):
    memory.content = memory_update.content
    memory.source = memory_update.source

    # Re-extract metadata whenever the memory changes
    extraction = extraction_service.extract(memory.content)

    # Rebuild knowledge graph
    graph = graph_builder.build(extraction)

    # Update graph in Neo4j
    neo4j_service.save_graph(graph)

    # Regenerate embedding
    memory.embedding = generate_embedding(memory.content)

    # Update extracted metadata
    memory.extracted_data = extraction.model_dump()

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
            Memory.embedding.cosine_distance(query_embedding).label("distance"),
        )
        .filter(Memory.user_id == user_id)
        .order_by(Memory.embedding.cosine_distance(query_embedding))
        .limit(top_k)
        .all()
    )

    return [
        {
            "id": memory.id,
            "content": memory.content,
            "source": memory.source,
            "similarity": round(1 - distance, 4),
        }
        for memory, distance in results
    ]