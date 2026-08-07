from collections import defaultdict

from app.schemas.document_search import (
    DocumentSearchResult,
)


class MultiDocumentRetrievalService:
    """
    Groups retrieved chunks by document.
    """

    def group_by_document(
        self,
        results: list[DocumentSearchResult],
    ) -> dict[str, list[DocumentSearchResult]]:

        grouped = defaultdict(list)

        for result in results:
            grouped[result.document_name].append(
                result
            )

        return dict(grouped)


multi_document_retrieval_service = (
    MultiDocumentRetrievalService()
)