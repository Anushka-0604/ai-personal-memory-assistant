from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models.memory import Memory
from ..schemas.memory import MemoryCreate, MemoryResponse, MemoryUpdate
from ..services.memory_service import (
    create_memory,
    get_memories,
    get_memory_by_id,
    update_memory,
    delete_memory,
)

from ..core.security import (
    authenticate_user,
    create_access_token,
    hash_password,
)
from ..database.dependencies import get_db, get_current_user
from ..models.user import User
from ..schemas.user import (
    MessageResponse,
    TokenResponse,
    UserCreate,
)

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Hello from AI Personal Memory Assistant Backend!"
    }


@router.post("/register", response_model=MessageResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

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


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }

@router.post(
    "/memories",
    response_model=MemoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_memory(
    memory: MemoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_memory(
        db=db,
        user_id=current_user.id,
        memory=memory,
    )

@router.get(
    "/memories",
    response_model=list[MemoryResponse],
)
def get_all_memories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_memories(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/memories/{memory_id}",
    response_model=MemoryResponse,
)
def get_single_memory(
    memory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memory = get_memory_by_id(
        db=db,
        memory_id=memory_id,
        user_id=current_user.id,
    )

    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found.",
        )

    return memory

@router.put(
    "/memories/{memory_id}",
    response_model=MemoryResponse,
)
def update_existing_memory(
    memory_id: int,
    memory_update: MemoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memory = get_memory_by_id(
        db=db,
        memory_id=memory_id,
        user_id=current_user.id,
    )

    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found.",
        )

    return update_memory(
        db=db,
        memory=memory,
        memory_update=memory_update,
    )
@router.delete(
    "/memories/{memory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_memory(
    memory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memory = get_memory_by_id(
        db=db,
        memory_id=memory_id,
        user_id=current_user.id,
    )

    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found.",
        )

    delete_memory(
        db=db,
        memory=memory,
    )