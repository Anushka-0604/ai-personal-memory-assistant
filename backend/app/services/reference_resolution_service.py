from typing import List

from app.models.chat_message import ChatMessage


class ReferenceResolutionService:
    """
    Service responsible for resolving references
    like 'it', 'this', 'that', etc.
    """

    REFERENCE_WORDS = {
        "it",
        "this",
        "that",
        "these",
        "those",
        "he",
        "she",
        "they",
        "them",
    }

    @staticmethod
    def resolve_reference(
        question: str,
        conversation_history: List[ChatMessage],
    ) -> str:
        """
        Resolve simple references using the most recent
        user message.
        """

        words = question.lower().split()

        has_reference = any(
            word.strip(".,?!") in ReferenceResolutionService.REFERENCE_WORDS
            for word in words
        )

        if not has_reference:
            return question

        previous_user_messages = [
            message
            for message in reversed(conversation_history)
            if message.role == "user"
        ]

        if not previous_user_messages:
            return question

        previous_message = previous_user_messages[0].content

        return (
            f'Previous user message: "{previous_message}"\n'
            f'Current question: "{question}"'
        )