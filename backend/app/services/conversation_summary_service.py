from typing import List

from app.core.config import (
    CONVERSATION_SUMMARIZATION_THRESHOLD,
)
from app.models.chat_message import ChatMessage


class ConversationSummaryService:
    """
    Generates a lightweight summary
    of a conversation.
    """

    @staticmethod
    def generate_summary(
        conversation_history: List[ChatMessage],
    ) -> str:
        """
        Summarize only long conversations.
        Short conversations are returned as-is.
        """

        if not conversation_history:
            return "No previous conversation."

        # For short conversations, keep everything.
        if (
            len(conversation_history)
            <= CONVERSATION_SUMMARIZATION_THRESHOLD
        ):
            return "\n".join(
                f"{message.role.capitalize()}: {message.content}"
                for message in conversation_history
            )

        # For long conversations, keep only the latest messages.
        recent_messages = conversation_history[
            -CONVERSATION_SUMMARIZATION_THRESHOLD:
        ]

        summary = [
            "Previous conversation has been summarized.",
            "",
            "Recent conversation:",
        ]

        summary.extend(
            f"{message.role.capitalize()}: {message.content}"
            for message in recent_messages
        )

        return "\n".join(summary)