from app.services.embedding_service import generate_embedding


class DiversificationService:
    """
    Diversifies retrieval results by removing
    highly similar memories using embedding
    cosine similarity.

    This prevents multiple nearly identical
    memories from appearing in the final results.
    """

    def __init__(
        self,
        similarity_threshold: float = 0.90,
    ):
        self.similarity_threshold = similarity_threshold

    def cosine_similarity(
        self,
        embedding1,
        embedding2,
    ):
        """
        Compute cosine similarity between
        two embeddings.
        """

        dot_product = sum(
            a * b
            for a, b in zip(
                embedding1,
                embedding2,
            )
        )

        norm1 = (
            sum(a * a for a in embedding1)
        ) ** 0.5

        norm2 = (
            sum(b * b for b in embedding2)
        ) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (
            norm1 * norm2
        )

    def diversify(
        self,
        results,
    ):
        """
        Remove highly similar memories while
        preserving the highest-ranked result.
        """

        diversified = []

        for candidate in results:

            candidate_embedding = (
                candidate["memory"].embedding
            )

            keep = True

            for selected in diversified:

                similarity = self.cosine_similarity(
                    candidate_embedding,
                    selected["memory"].embedding,
                )

                if (
                    similarity
                    >= self.similarity_threshold
                ):
                    keep = False
                    break

            if keep:
                diversified.append(candidate)

        return diversified


diversification_service = (
    DiversificationService()
)