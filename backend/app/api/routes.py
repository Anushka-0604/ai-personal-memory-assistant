from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..models.memory import Memory
from ..models.chat_session import ChatSession
from ..models.user import User

from ..schemas.memory import (
    MemoryCreate,
    MemoryResponse,
    MemoryUpdate,
    MemorySearchRequest,
    MemorySearchResult,
)

from ..schemas.user import (
    MessageResponse,
    TokenResponse,
    UserCreate,
)

from ..schemas.chat import ChatRequest, ChatResponse

from ..schemas.chat_session import (
    ChatSessionCreate,
    ChatSessionResponse,
)

from ..schemas.chat_message import (
    ChatMessageCreate,
    ChatMessageResponse,
)

from ..services.memory_service import (
    create_memory,
    get_memories,
    get_memory_by_id,
    update_memory,
    delete_memory,
    search_memories,
)

from ..services.chat_session_service import (
    create_chat_session,
    get_chat_sessions,
    get_chat_session_by_id,
    delete_chat_session,
)

from ..services.chat_message_service import (
    create_chat_message,
    get_chat_messages,
)

from ..services.chat_service import ChatService

from ..core.security import (
    authenticate_user,
    create_access_token,
    hash_password,
)

from ..database.dependencies import (
    get_db,
    get_current_user,
)

router = APIRouter()
chat_service = ChatService()


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
@router.post(
    "/memories/search",
    response_model=list[MemorySearchResult],
)
def semantic_search(
    request: MemorySearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return search_memories(
        db=db,
        user_id=current_user.id,
        query=request.query,
        top_k=request.top_k,
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

@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return chat_service.chat(
        db=db,
        user_id=current_user.id,
        session_id=request.session_id,
        question=request.question,
        top_k=request.top_k,
    )

@router.post(
    "/chat/sessions",
    response_model=ChatSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_chat_session(
    session: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_chat_session(
        db=db,
        user_id=current_user.id,
        session=session,
    )

@router.get(
    "/chat/sessions",
    response_model=list[ChatSessionResponse],
)
def get_all_chat_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_chat_sessions(
        db=db,
        user_id=current_user.id,
    )
@router.get(
    "/chat/sessions/{session_id}",
    response_model=ChatSessionResponse,
)
def get_single_chat_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = get_chat_session_by_id(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found.",
        )

    return session

@router.delete(
    "/chat/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_chat_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = get_chat_session_by_id(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found.",
        )

    delete_chat_session(
        db=db,
        session=session,
    )

@router.post(
    "/chat/sessions/{session_id}/messages",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_chat_message(
    session_id: int,
    message: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = get_chat_session_by_id(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found.",
        )

    return create_chat_message(
        db=db,
        session_id=session.id,
        message=message,
    )
@router.get(
    "/chat/sessions/{session_id}/messages",
    response_model=list[ChatMessageResponse],
)
def get_all_chat_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = get_chat_session_by_id(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found.",
        )

    return get_chat_messages(
        db=db,
        session_id=session.id,
    )