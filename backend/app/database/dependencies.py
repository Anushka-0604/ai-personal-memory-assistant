from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .connection import SessionLocal
from ..core.security import oauth2_scheme, verify_access_token
from ..models.user import User


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    email = verify_access_token(token)

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user