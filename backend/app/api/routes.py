from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.user import UserCreate
from ..models.user import User
from ..core.security import hash_password
from ..database.dependencies import get_db

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Hello from AI Personal Memory Assistant Backend!"}

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return {
            "message": "Email already registered!"
        }

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully!"
    }