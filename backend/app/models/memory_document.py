from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..database.base import Base


class MemoryDocument(Base):
    __tablename__ = "memory_documents"

    memory_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "memories.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    document_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )