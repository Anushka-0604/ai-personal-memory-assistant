from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.schemas.chat_message import ChatMessageCreate


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