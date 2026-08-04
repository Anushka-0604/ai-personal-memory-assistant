from typing import List


class ConversationMemoryService:
    """
    Combines retrieved context with
    recent conversation context.
    """

    @staticmethod
    def build_context(
        memories: List[str],
        conversation_summary: str,
    ) -> str:
        """
        Build a single context string for the LLM.
        """

        context_section = "\n".join(
            f"- {item}"
            for item in memories
        )

        return (
            f"Conversation Summary:\n"
            f"{conversation_summary}\n\n"
            f"Retrieved Context:\n"
            f"{context_section}"
        )