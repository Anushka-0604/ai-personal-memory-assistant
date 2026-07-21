from typing import List

from app.core.config import (
    CONVERSATION_SUMMARIZATION_THRESHOLD,
)
from app.models.chat_message import ChatMessage
from app.services.llm_service import LLMService
from app.services.prompt_builder import PromptBuilder


class ConversationSummaryService:
    """
    Generates AI-powered summaries of conversations.

    Short conversations are returned as-is to avoid
    unnecessary LLM calls.

    Long conversations are summarized using the LLM.
    """

    llm_service = LLMService()

    @staticmethod
    def generate_summary(
        conversation_history: List[ChatMessage],
    ) -> str:
        """
        Generate a conversation summary.

        - Short conversations:
            Return the formatted conversation.
        - Long conversations:
            Generate an AI summary.
        """

        if not conversation_history:
            return "No previous conversation."

        formatted_conversation = "\n".join(
            f"{message.role.capitalize()}: {message.content}"
            for message in conversation_history
        )

        # Keep short conversations unchanged
        if (
            len(conversation_history)
            <= CONVERSATION_SUMMARIZATION_THRESHOLD
        ):
            return formatted_conversation

        # Build AI summarization prompt
        prompt = PromptBuilder.build_summary_prompt(
            formatted_conversation
        )

        try:
            summary = (
                ConversationSummaryService.llm_service.generate_response(
                    prompt
                )
            )

            if summary and summary.strip():
                return summary.strip()

        except Exception:
            pass

        # -----------------------------
        # Fallback (if LLM fails)
        # -----------------------------
        recent_messages = conversation_history[
            -CONVERSATION_SUMMARIZATION_THRESHOLD:
        ]

        fallback_summary = [
            "Previous conversation has been summarized.",
            "",
            "Recent conversation:",
        ]

        fallback_summary.extend(
            f"{message.role.capitalize()}: {message.content}"
            for message in recent_messages
        )

        return "\n".join(fallback_summary)