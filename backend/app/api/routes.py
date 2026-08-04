# routes.py
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..services.dashboard_service import dashboard_service
from ..services.review_service import review_service
from ..schemas.review import ReviewMemory
from ..schemas.dashboard import DashboardSummary
from ..services.health_service import health_service
from ..services.recommendation_service import recommendation_service
from ..services.analytics_service import analytics_service
from ..schemas.recommendation import RecommendedMemory
from ..schemas.analytics import (
    MemoryStatistics,
    CategoryDistribution,
)
from ..services.ai_dashboard_service import (
    ai_dashboard_service,
)
from ..schemas.ai_dashboard import (
    AIDashboardResponse,
)
from ..services.usage_dashboard_service import (
    usage_dashboard_service,
)
from ..schemas.usage_dashboard import (
    UsageDashboard,
)
from ..services.retrieval_quality_service import (
    retrieval_quality_service,
)
from ..schemas.retrieval_quality import (
    RetrievalQualityResponse,
)
from ..models.system_metric import SystemMetric
from ..services.retrieval_analytics_service import (
    retrieval_analytics_service,
)
from ..models.retrieval_log import RetrievalLog
from ..services.memory_analytics_service import (
    memory_analytics_service,
)
from ..schemas.document import (
    DocumentResponse,
)

from ..schemas.document_search import (
    DocumentSearchResult,
)

from ..services.document_service import (
    create_document,
)

from ..services.file_storage_service import (
    save_file,
)

from ..services.document_search_service import (
    semantic_document_search,
)

from ..schemas.memory_analytics import (
    MemoryAnalyticsResponse,
)
from ..services.evaluation_service import EvaluationService
from ..models.ai_request_log import AIRequestLog
from app.schemas.insights import MemoryInsights
from app.services import insights_service
from datetime import date
from ..schemas.timeline import TimelineMemory
from ..services.timeline_service import timeline_service
from app.services.graph_query_service import graph_query_service
from app.services.temporal_query_service import temporal_query_service

from ..models.memory import Memory
from ..models.chat_session import ChatSession
from ..models.user import User
from ..models.user_interaction import InteractionType

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

from ..schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from ..schemas.chat_session import (
    ChatSessionCreate,
    ChatSessionUpdate,
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
    update_chat_session,
    delete_chat_session,
)

from ..services.chat_message_service import (
    create_chat_message,
    get_chat_messages,
)

from ..services.chat_service import ChatService
from ..services.interaction_service import interaction_service

from ..core.security import (
    authenticate_user,
    create_access_token,
    hash_password,
)

from ..database.dependencies import (
    get_db,
    get_current_user,
)

from datetime import date, timedelta

router = APIRouter()
chat_service = ChatService()


@router.get("/")
def root():
    return {
        "message": "Hello from AI Personal Memory Assistant Backend!"
    }


@router.post(
    "/register",
    response_model=MessageResponse,
)
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


@router.post(
    "/login",
    response_model=TokenResponse,
)
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


@router.post(
    "/documents/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_info = save_file(file)

    document = create_document(
        db=db,
        user_id=current_user.id,
        filename=file_info["filename"],
        original_filename=file_info["original_filename"],
        file_type=file_info["file_type"],
        file_size=file_info["file_size"],
        file_path=file_info["file_path"],
    )

    return document


@router.post(
    "/documents/search",
    response_model=list[DocumentSearchResult],
)
def search_documents(
    query: str,
    top_k: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = semantic_document_search(
        db=db,
        query=query,
        top_k=top_k,
    )

    response = []

    for chunk, distance in results:

        response.append(
            DocumentSearchResult(
                document_id=chunk.document_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                similarity=round(
                    max(0.0, 1 - distance),
                    4,
                ),
            )
        )

    return response

@router.get("/memories/today")
def get_today_memories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()

    return temporal_query_service.get_memories_for_date(
        db=db,
        user_id=current_user.id,
        target_date=today,
    )


@router.get("/memories/tomorrow")
def get_tomorrow_memories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tomorrow = date.today() + timedelta(days=1)

    return temporal_query_service.get_memories_for_date(
        db=db,
        user_id=current_user.id,
        target_date=tomorrow,
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

    interaction_service.record_interaction(
        db=db,
        user_id=current_user.id,
        memory_id=memory.id,
        interaction_type=InteractionType.VIEW,
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

    updated_memory = update_memory(
        db=db,
        memory=memory,
        memory_update=memory_update,
    )

    interaction_service.record_interaction(
        db=db,
        user_id=current_user.id,
        memory_id=updated_memory.id,
        interaction_type=InteractionType.UPDATE,
    )

    return updated_memory


@router.post(
    "/memories/search",
    response_model=list[MemorySearchResult],
)
def semantic_search(
    request: MemorySearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = search_memories(
        db=db,
        user_id=current_user.id,
        query=request.query,
        top_k=request.top_k,
        conversation_history=request.conversation_history,
        category=request.category,
        sentiment=request.sentiment,
        tags=request.tags,
        start_date=request.start_date,
        end_date=request.end_date,
    )

    for memory in results:
        interaction_service.record_interaction(
            db=db,
            user_id=current_user.id,
            memory_id=memory["id"],
            interaction_type=InteractionType.SEARCH,
        )

    return results


@router.get(
    "/analytics/statistics",
    response_model=MemoryStatistics,
)
def get_memory_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return analytics_service.get_memory_statistics(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/analytics/categories",
    response_model=list[CategoryDistribution],
)
def get_category_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return analytics_service.get_category_distribution(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/dashboard/summary",
    response_model=DashboardSummary,
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return dashboard_service.get_dashboard_summary(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/insights",
    response_model=MemoryInsights,
)
def get_memory_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return insights_service.get_memory_insights(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/recommendations",
    response_model=list[RecommendedMemory],
)
def get_recommendations(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return recommendation_service.get_recommended_memories(
        db=db,
        user_id=current_user.id,
        limit=limit,
    )


@router.get(
    "/review-queue",
    response_model=list[ReviewMemory],
)
def get_review_queue(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.get_review_queue(
        db=db,
        user_id=current_user.id,
        limit=limit,
    )


@router.get(
    "/timeline",
    response_model=list[TimelineMemory],
)
def get_timeline(
    limit: int = 20,
    page: int = 1,
    category: str | None = None,
    search: str | None = None,
    include_archived: bool = False,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return timeline_service.get_timeline(
        db=db,
        user_id=current_user.id,
        limit=limit,
        page=page,
        category=category,
        search=search,
        include_archived=include_archived,
        start_date=start_date,
        end_date=end_date,
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

    interaction_service.record_interaction(
        db=db,
        user_id=current_user.id,
        memory_id=memory.id,
        interaction_type=InteractionType.DELETE,
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


@router.put(
    "/chat/sessions/{session_id}",
    response_model=ChatSessionResponse,
)
def update_existing_chat_session(
    session_id: int,
    session_update: ChatSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = get_chat_session_by_id(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )

    return update_chat_session(
        db=db,
        session=session,
        session_update=session_update,
    )


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


# =====================================================
# Knowledge Graph APIs
# =====================================================

@router.get("/graph/people")
def get_people():
    return {
        "people": graph_query_service.get_people(),
    }


@router.get("/graph/organizations")
def get_organizations():
    return {
        "organizations": graph_query_service.get_organizations(),
    }


@router.get("/graph/locations")
def get_locations():
    return {
        "locations": graph_query_service.get_locations(),
    }


@router.get("/graph/person/{person_name}/organizations")
def get_organizations_for_person(person_name: str):
    return {
        "person": person_name,
        "organizations": graph_query_service.get_organizations_for_person(
            person_name
        ),
    }


@router.get("/graph/organization/{organization_name}/people")
def get_people_for_organization(organization_name: str):
    return {
        "organization": organization_name,
        "people": graph_query_service.get_people_for_organization(
            organization_name
        ),
    }


@router.get("/graph/person/{person_name}/locations")
def get_locations_for_person(person_name: str):
    return {
        "person": person_name,
        "locations": graph_query_service.get_locations_for_person(
            person_name
        ),
    }


@router.get("/graph/location/{location_name}/people")
def get_people_for_location(location_name: str):
    return {
        "location": location_name,
        "people": graph_query_service.get_people_for_location(
            location_name
        ),
    }


@router.get("/graph/organization/{organization_name}/locations")
def get_locations_for_organization(
    organization_name: str,
):
    return {
        "organization": organization_name,
        "locations": graph_query_service.get_locations_for_organization(
            organization_name
        ),
    }


@router.get("/graph/location/{location_name}/organizations")
def get_organizations_for_location(
    location_name: str,
):
    return {
        "location": location_name,
        "organizations": graph_query_service.get_organizations_for_location(
            location_name
        ),
    }

@router.get("/evaluation/latest")
def get_latest_evaluations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(AIRequestLog)
        .filter(AIRequestLog.user_id == current_user.id)
        .order_by(AIRequestLog.created_at.desc())
        .limit(20)
        .all()
    )

@router.get("/evaluation/latest")
def get_latest_evaluations(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return EvaluationService.get_latest(
        db=db,
        user_id=current_user.id,
        limit=limit,
    )


@router.get("/evaluation/summary")
def get_evaluation_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return EvaluationService.get_summary(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/analytics/memory",
    response_model=MemoryAnalyticsResponse,
)
def get_memory_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return memory_analytics_service.get_statistics(
        db=db,
        user_id=current_user.id,
    )
@router.get("/analytics/retrieval")
def get_retrieval_logs(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(RetrievalLog)
        .filter(RetrievalLog.user_id == current_user.id)
        .order_by(RetrievalLog.created_at.desc())
        .limit(limit)
        .all()
    )
@router.get("/analytics/system-metrics")
def get_system_metrics(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(SystemMetric)
        .order_by(SystemMetric.created_at.desc())
        .limit(limit)
        .all()
    )

@router.get("/system/health")
def system_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return health_service.get_health(db)

@router.get(
    "/analytics/retrieval-quality",
    response_model=RetrievalQualityResponse,
)
def get_retrieval_quality(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return retrieval_quality_service.calculate_quality(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/analytics/usage-dashboard",
    response_model=UsageDashboard,
)
def get_usage_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return usage_dashboard_service.get_dashboard(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/analytics/ai-dashboard",
    response_model=AIDashboardResponse,
)
def get_ai_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ai_dashboard_service.get_dashboard(
        db=db,
        user_id=current_user.id,
    )