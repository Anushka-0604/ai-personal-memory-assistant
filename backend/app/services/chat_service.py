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
from app.services.llm_service import LLMService
from app.services.memory_service import search_memories
from app.services.prompt_builder import PromptBuilder


class ChatService:
    """
    Responsible for orchestrating the complete RAG pipeline.
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
        # Save user's message
        create_chat_message(
            db=db,
            session_id=session_id,
            message=ChatMessageCreate(
                role="user",
                content=question,
            ),
        )

        # Load recent conversation messages
        conversation_messages = (
            ConversationContextService.get_recent_messages(
                db=db,
                session_id=session_id,
                limit=CONVERSATION_HISTORY_LIMIT,
            )
        )

        # Format conversation for Prompt Builder
        conversation_history = (
            ConversationContextService.format_conversation(
                conversation_messages
            )
        )

        # Retrieve relevant memories
        memories = search_memories(
            db=db,
            user_id=user_id,
            query=question,
            top_k=top_k,
        )

        # Select the best memories
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

        memory_texts = [
            memory["content"]
            for memory in selected_memories
        ]

        prompt = PromptBuilder.build_prompt(
            user_question=question,
            memories=memory_texts,
            conversation_history=conversation_history,
        )

        # Generate response from the LLM
        try:
            answer = self.llm_service.generate_response(
                prompt
            )

        except Exception:
            answer = (
                "I'm sorry, but I couldn't generate a response "
                "at the moment. Please try again later."
            )

        # Save assistant's response
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