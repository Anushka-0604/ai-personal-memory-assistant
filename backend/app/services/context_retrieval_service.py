class ContextRetrievalService:
    """
    Expands the current query
    using conversation history.
    """

    def build_query(
        self,
        query: str,
        history: list[str] | None = None,
    ) -> str:

        if not history:
            return query

        history = history[-3:]

        context = " ".join(history)

        return f"{context} {query}"


context_retrieval_service = (
    ContextRetrievalService()
)