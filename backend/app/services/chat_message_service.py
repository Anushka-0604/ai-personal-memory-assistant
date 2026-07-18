from datetime import datetime

from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.models.chat_session import ChatSession
from app.schemas.chat_message import ChatMessageCreate


MAX_CHAT_HISTORY = 10


def create_chat_message(
    db: Session,
    session_id: int,
    message: ChatMessageCreate,
):
    new_message = ChatMessage(
        session_id=session_id,
        role=message.role,
        content=message.content,
    )

    db.add(new_message)

    # Update the chat session's last activity time
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if session:
        session.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(new_message)

    return new_message


def get_chat_messages(
    db: Session,
    session_id: int,
):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )


def get_conversation_history(
    db: Session,
    session_id: int,
) -> str:
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(MAX_CHAT_HISTORY)
        .all()
    )

    if not messages:
        return ""

    # Restore chronological order
    messages.reverse()

    history = []

    for message in messages:
        history.append(
            f"{message.role.capitalize()}: {message.content}"
        )

    return "\n".join(history)