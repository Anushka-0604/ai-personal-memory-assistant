from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ..database.base import Base


class AIRequestLog(Base):
    __tablename__ = "ai_request_logs"

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

    chat_session_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("chat_sessions.id"),
        nullable=True,
    )

    query: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    retrieval_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    selected_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    average_similarity: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    average_importance: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    average_context_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    precision_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    recall_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    response_generated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    response_length: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    embedding_time_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    retrieval_time_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    ranking_time_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    context_time_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    prompt_time_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    llm_time_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    total_time_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User")

    chat_session: Mapped["ChatSession"] = relationship("ChatSession")