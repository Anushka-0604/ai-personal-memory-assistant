from typing import List

from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage


class ConversationContextService:
    """
    Service responsible for loading and formatting conversation history.
    """

    @staticmethod
    def get_recent_messages(
        db: Session,
        session_id: int,
        limit: int = 10,
    ) -> List[ChatMessage]:
        """
        Retrieve the most recent messages for a chat session.
        Returns them in chronological order.
        """

        messages = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
            .all()
        )

        return list(reversed(messages))

    @staticmethod
    def format_conversation(
        messages: List[ChatMessage],
    ) -> str:
        """
        Convert chat messages into a formatted conversation string
        for the Prompt Builder.
        """

        if not messages:
            return ""

        conversation = []

        for message in messages:
            role = message.role.capitalize()
            conversation.append(
                f"{role}: {message.content}"
            )

        return "\n".join(conversation)