from typing import List

from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage


class ConversationContextService:
    """
    Service responsible for loading conversation history.
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