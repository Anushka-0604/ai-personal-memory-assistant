from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ..database.base import Base


class InteractionType(str, Enum):
    SEARCH = "SEARCH"
    VIEW = "VIEW"
    CHAT_REFERENCE = "CHAT_REFERENCE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    FAVORITE = "FAVORITE"
    ARCHIVE = "ARCHIVE"


class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    memory_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("memories.id"),
        nullable=False,
    )

    interaction_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    weight: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="interactions",
    )

    memory: Mapped["Memory"] = relationship(
        "Memory",
        back_populates="interactions",
    )