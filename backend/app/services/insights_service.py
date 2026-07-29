from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.memory import Memory


def get_memory_insights(db: Session, user_id: int):
    total_memories = (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .count()
    )

    archived_memories = (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id,
            Memory.is_archived == True,
        )
        .count()
    )

    forgotten_memories = (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id,
            Memory.is_forgotten == True,
        )
        .count()
    )

    total_categories = (
        db.query(Memory.category)
        .filter(
            Memory.user_id == user_id,
            Memory.category.isnot(None),
        )
        .distinct()
        .count()
    )

    category_row = (
        db.query(
            Memory.category,
            func.count(Memory.id).label("count"),
        )
        .filter(
            Memory.user_id == user_id,
            Memory.category.isnot(None),
        )
        .group_by(Memory.category)
        .order_by(func.count(Memory.id).desc())
        .first()
    )

    important_memory = (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .order_by(Memory.importance.desc())
        .first()
    )

    accessed_memory = (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .order_by(Memory.access_count.desc())
        .first()
    )

    newest_memory = (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .order_by(Memory.created_at.desc())
        .first()
    )

    return {
        "total_memories": total_memories,
        "total_categories": total_categories,
        "archived_memories": archived_memories,
        "forgotten_memories": forgotten_memories,
        "most_used_category": category_row.category if category_row else None,
        "most_important_memory": important_memory.content if important_memory else None,
        "most_accessed_memory": accessed_memory.content if accessed_memory else None,
        "newest_memory": newest_memory.content if newest_memory else None,
    }