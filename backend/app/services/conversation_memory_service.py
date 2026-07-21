from typing import List


class ConversationMemoryService:
    """
    Combines long-term memories with
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

        memory_section = "\n".join(
            f"- {memory}"
            for memory in memories
        )

        return (
            f"Conversation Summary:\n"
            f"{conversation_summary}\n\n"
            f"Relevant Memories:\n"
            f"{memory_section}"
        )