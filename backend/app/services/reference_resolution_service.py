from typing import List

from app.models.chat_message import ChatMessage


class ReferenceResolutionService:
    """
    Service responsible for resolving references
    like 'it', 'this', 'that', etc.
    """

    @staticmethod
    def resolve_reference(
        question: str,
        conversation_history: List[ChatMessage],
    ) -> str:
        """
        Currently returns the original question.
        Reference resolution logic will be added
        in the next step.
        """
        return question