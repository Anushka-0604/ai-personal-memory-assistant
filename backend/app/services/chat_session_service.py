from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession
from app.schemas.chat_session import (
    ChatSessionCreate,
    ChatSessionUpdate,
)


def create_chat_session(
    db: Session,
    user_id: int,
    session: ChatSessionCreate,
):
    new_session = ChatSession(
        user_id=user_id,
        title=session.title,
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


def get_chat_sessions(
    db: Session,
    user_id: int,
):
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.updated_at.desc())
        .all()
    )


def get_chat_session_by_id(
    db: Session,
    session_id: int,
    user_id: int,
):
    return (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id,
        )
        .first()
    )


def update_chat_session(
    db: Session,
    session: ChatSession,
    session_update: ChatSessionUpdate,
):
    session.title = session_update.title

    db.commit()
    db.refresh(session)

    return session


def delete_chat_session(
    db: Session,
    session: ChatSession,
):
    db.delete(session)
    db.commit()