from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Header, HTTPException, status
from ..core.config import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.user import (
    UserCreate,
    MessageResponse,
    TokenResponse,
)
from ..models.user import User
from ..core.security import (
    hash_password,
    authenticate_user,
    create_access_token,
)
from ..database.dependencies import get_db

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Hello from AI Personal Memory Assistant Backend!"}

@router.post("/register", response_model=MessageResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
    )

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
@router.post("/login", response_model=TokenResponse)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    authenticated_user = authenticate_user(
    form_data.username,
    form_data.password,
    db,
)

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
    )

    access_token = create_access_token(
        {
            "sub": authenticated_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

# @router.get("/me")
# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db),
# ):
#     try:
#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM],
#         )

#         email = payload.get("sub")

#         if email is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token",
#             )

#         user = db.query(User).filter(User.email == email).first()

#         if user is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User not found",
#             )

#         return {
#             "id": user.id,
#             "name": user.name,
#             "email": user.email,
#         }

#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#         )

@router.get("/me")
def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    try:
        token = authorization.replace("Bearer ", "")

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user = db.query(User).filter(User.email == email).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )