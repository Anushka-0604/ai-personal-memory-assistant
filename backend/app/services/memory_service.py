from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.schemas.memory import MemoryCreate, MemoryUpdate
from app.services.embedding_service import generate_embedding


def create_memory(db: Session, user_id: int, memory: MemoryCreate):
    embedding = generate_embedding(memory.content)

    new_memory = Memory(
        user_id=user_id,
        content=memory.content,
        source=memory.source,
        embedding=embedding,
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
    memory.embedding = generate_embedding(memory.content)

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