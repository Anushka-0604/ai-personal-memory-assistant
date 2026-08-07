from sqlalchemy.orm import Session

from app.services.document_context_service import (
    document_context_service,
)
from app.services.document_search_service import (
    semantic_document_search,
)


class DocumentRAGService:
    """
    Builds document context for LLMs.
    """

    def build_context(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
    ) -> str:

        results = semantic_document_search(
            db=db,
            query=query,
            top_k=top_k,
        )

        return document_context_service.build_context(
            results
        )


document_rag_service = (
    DocumentRAGService()
)