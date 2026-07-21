class ConversationRetrievalService:
    """
    Builds a conversation-aware query
    for semantic memory retrieval.
    """

    @staticmethod
    def build_search_query(
        resolved_question: str,
        conversation_history: str,
    ) -> str:
        """
        Combines conversation history with
        the resolved user question.
        """

        if not conversation_history:
            return resolved_question

        return (
            f"{conversation_history}\n\n"
            f"Current Question:\n"
            f"{resolved_question}"
        )