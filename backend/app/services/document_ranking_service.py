from app.schemas.document_search import (
    DocumentSearchResult,
)


class DocumentRankingService:
    """
    Re-ranks retrieved document chunks.
    """

    def rank(
        self,
        results: list[DocumentSearchResult],
    ) -> list[DocumentSearchResult]:

        return sorted(
            results,
            key=self._score,
            reverse=True,
        )

    def _score(
        self,
        result: DocumentSearchResult,
    ) -> float:
        """
        Composite ranking score.

        Current implementation:
        - Semantic similarity

        Future:
        - Metadata score
        - Freshness
        - User interactions
        - Citation importance
        """

        semantic_score = result.similarity

        return semantic_score


document_ranking_service = (
    DocumentRankingService()
)