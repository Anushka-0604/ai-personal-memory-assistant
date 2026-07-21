from sqlalchemy.orm import Session

from app.core.config import (
    CONVERSATION_HISTORY_LIMIT,
    RAG_SIMILARITY_THRESHOLD,
)
from app.schemas.chat_message import ChatMessageCreate
from app.services.chat_message_service import create_chat_message
from app.services.context_selector import context_selector
from app.services.conversation_context_service import (
    ConversationContextService,
)
from app.services.conversation_memory_service import (
    ConversationMemoryService,
)
from app.services.conversation_retrieval_service import (
    ConversationRetrievalService,
)
from app.services.conversation_summary_service import (
    ConversationSummaryService,
)
from app.services.llm_service import LLMService
from app.services.memory_service import search_memories
from app.services.prompt_builder import PromptBuilder
from app.services.reference_resolution_service import (
    ReferenceResolutionService,
)


class ChatService:
    """
    Responsible for orchestrating the complete
    Retrieval-Augmented Generation (RAG) pipeline.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def chat(
        self,
        db: Session,
        user_id: int,
        session_id: int,
        question: str,
        top_k: int = 5,
    ):
        # -------------------------------------------------------------
        # Step 1: Load previous conversation
        # -------------------------------------------------------------
        conversation_messages = (
            ConversationContextService.get_recent_messages(
                db=db,
                session_id=session_id,
                limit=CONVERSATION_HISTORY_LIMIT,
            )
        )

        # -------------------------------------------------------------
        # Step 2: Resolve references
        # -------------------------------------------------------------
        resolved_question = (
            ReferenceResolutionService.resolve_reference(
                question=question,
                conversation_history=conversation_messages,
            )
        )

        # -------------------------------------------------------------
        # Step 3: Save current user message
        # -------------------------------------------------------------
        create_chat_message(
            db=db,
            session_id=session_id,
            message=ChatMessageCreate(
                role="user",
                content=question,
            ),
        )

        # -------------------------------------------------------------
        # Step 4: Reload conversation including latest message
        # -------------------------------------------------------------
        conversation_messages = (
            ConversationContextService.get_recent_messages(
                db=db,
                session_id=session_id,
                limit=CONVERSATION_HISTORY_LIMIT,
            )
        )

        # -------------------------------------------------------------
        # Step 5: Format conversation
        # -------------------------------------------------------------
        conversation_history = (
            ConversationContextService.format_conversation(
                conversation_messages
            )
        )

        # -------------------------------------------------------------
        # Step 6: Generate conversation summary
        # -------------------------------------------------------------
        conversation_summary = (
            ConversationSummaryService.generate_summary(
                conversation_messages
            )
        )

        # -------------------------------------------------------------
        # Step 7: Build conversation-aware search query
        # -------------------------------------------------------------
        search_query = (
            ConversationRetrievalService.build_search_query(
                resolved_question=resolved_question,
                conversation_history=conversation_history,
            )
        )

        # -------------------------------------------------------------
        # Step 8: Retrieve memories
        # -------------------------------------------------------------
        memories = search_memories(
            db=db,
            user_id=user_id,
            query=search_query,
            top_k=top_k,
        )

        # -------------------------------------------------------------
        # Step 9: Select relevant memories
        # -------------------------------------------------------------
        selected_memories = context_selector.select(
            memories=memories,
            similarity_threshold=RAG_SIMILARITY_THRESHOLD,
            max_memories=top_k,
        )

        if not selected_memories:
            answer = (
                "I couldn't find any relevant memories "
                "to answer your question."
            )

            create_chat_message(
                db=db,
                session_id=session_id,
                message=ChatMessageCreate(
                    role="assistant",
                    content=answer,
                ),
            )

            return {
                "answer": answer,
                "retrieved_memories": [],
            }

        # -------------------------------------------------------------
        # Step 10: Extract memory text
        # -------------------------------------------------------------
        memory_texts = [
            memory["content"]
            for memory in selected_memories
        ]

        # -------------------------------------------------------------
        # Step 11: Build unified context
        # -------------------------------------------------------------
        context = (
            ConversationMemoryService.build_context(
                memories=memory_texts,
                conversation_summary=conversation_summary,
            )
        )

        # -------------------------------------------------------------
        # Step 12: Build chat prompt
        # -------------------------------------------------------------
        prompt = PromptBuilder.build_chat_prompt(
            user_question=resolved_question,
            context=context,
        )

        # -------------------------------------------------------------
        # Step 13: Generate AI response
        # -------------------------------------------------------------
        try:
            print("\n========== FINAL PROMPT ==========")
            print(prompt)
            print("==================================\n")

            answer = self.llm_service.generate_response(
                prompt
            )

        except Exception:
            answer = (
                "I'm sorry, but I couldn't generate a response "
                "at the moment. Please try again later."
            )

        # -------------------------------------------------------------
        # Step 14: Save assistant response
        # -------------------------------------------------------------
        create_chat_message(
            db=db,
            session_id=session_id,
            message=ChatMessageCreate(
                role="assistant",
                content=answer,
            ),
        )

        return {
            "answer": answer,
            "retrieved_memories": selected_memories,
        }