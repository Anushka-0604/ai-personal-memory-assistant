from sentence_transformers import CrossEncoder


class CrossEncoderService:
    """
    Re-ranks retrieved memories using a CrossEncoder model.
    """

    def __init__(self):
        print("Loading CrossEncoder model...")

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        print("CrossEncoder loaded successfully.")

    def rerank(
        self,
        query: str,
        memories: list[str],
    ) -> list[float]:
        """
        Returns one relevance score per memory.
        """

        if not memories:
            return []

        pairs = [
            (query, memory)
            for memory in memories
        ]

        scores = self.model.predict(pairs)

        return scores.tolist()


cross_encoder_service = CrossEncoderService()