import time

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
from app.services.document_search_service import (
    semantic_document_search,
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
from app.services.evaluation_service import EvaluationService
from app.services.llm_service import LLMService
from app.services.memory_service import search_memories
from app.services.observability_service import (
    observability_service,
)
from app.services.prompt_builder import PromptBuilder
from app.services.reference_resolution_service import (
    ReferenceResolutionService,
)
from app.services.retrieval_analytics_service import (
    retrieval_analytics_service,
)
from app.services.system_metric_service import (
    system_metric_service,
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
        total_start = observability_service.start_trace()

        retrieval_time = 0.0
        context_time = 0.0
        prompt_time = 0.0
        llm_time = 0.0

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
        retrieval_start = time.perf_counter()

        memories = search_memories(
            db=db,
            user_id=user_id,
            query=search_query,
            top_k=top_k,
        )

        document_chunks = semantic_document_search(
            db=db,
            query=search_query,
            top_k=top_k,
        )

        retrieval_time = (
            time.perf_counter() - retrieval_start
        ) * 1000

        observability_service.log_stage(
            "Retrieval",
            retrieval_time,
        )

        # -------------------------------------------------------------
        # Step 9: Select relevant memories
        # -------------------------------------------------------------
        context_start = time.perf_counter()

        selected_memories = context_selector.select(
            memories=memories,
            similarity_threshold=RAG_SIMILARITY_THRESHOLD,
            max_memories=top_k,
        )

        context_time = (
            time.perf_counter() - context_start
        ) * 1000

        observability_service.log_stage(
            "Context Selection",
            context_time,
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

            total_time = observability_service.end_trace(
                total_start
            )

            observability_service.log_stage(
                "Total Request",
                total_time,
            )

            EvaluationService.log_request(
                db=db,
                user_id=user_id,
                chat_session_id=session_id,
                query=question,
                retrieval_count=len(memories),
                selected_count=0,
                average_similarity=0.0,
                average_importance=0.0,
                average_context_score=0.0,
                precision_score=0.0,
                recall_score=0.0,
                response_generated=False,
                response_length=len(answer),
                embedding_time_ms=0.0,
                retrieval_time_ms=retrieval_time,
                ranking_time_ms=0.0,
                context_time_ms=context_time,
                prompt_time_ms=0.0,
                llm_time_ms=0.0,
                total_time_ms=total_time,
            )

            system_metric_service.log(
                db=db,
                metric_name="llm_response_time",
                metric_value=llm_time,
                unit="ms",
            )

            system_metric_service.log(
                db=db,
                metric_name="retrieval_time",
                metric_value=retrieval_time,
                unit="ms",
            )

            system_metric_service.log(
                db=db,
                metric_name="total_request_time",
                metric_value=total_time,
                unit="ms",
            )

            retrieval_analytics_service.log(
                db=db,
                user_id=user_id,
                chat_session_id=session_id,
                query=question,
                retrieved_count=len(memories),
                selected_count=0,
                average_similarity=0.0,
                retrieval_time_ms=retrieval_time,
            )

            return {
                "answer": answer,
                "retrieved_memories": [],
                "retrieved_documents": [
                    {
                        "document_id": chunk.document_id,
                        "chunk_index": chunk.chunk_index,
                        "content": chunk.content,
                        "similarity": round(
                            max(0.0, 1 - distance),
                            4,
                        ),
                    }
                    for chunk, distance in document_chunks
                ],
            }

        # -------------------------------------------------------------
        # Step 10: Extract memory text
        # -------------------------------------------------------------
        memory_texts = [
            memory["content"]
            for memory in selected_memories
        ]
        document_texts = [
            chunk.content
            for chunk, _ in document_chunks
        ]
        # -------------------------------------------------------------
        # Step 11: Build unified context
        # -------------------------------------------------------------
        context_start = time.perf_counter()

        combined_context = (
            memory_texts +
            document_texts
        )

        context = (
            ConversationMemoryService.build_context(
                memories=combined_context,
                conversation_summary=conversation_summary,
            )
        )

        context_time += (
            time.perf_counter() - context_start
        ) * 1000

        observability_service.log_stage(
            "Context Building",
            context_time,
        )

        # -------------------------------------------------------------
        # Step 12: Build chat prompt
        # -------------------------------------------------------------
        prompt_start = time.perf_counter()

        prompt = PromptBuilder.build_chat_prompt(
            user_question=resolved_question,
            context=context,
        )

        prompt_time = (
            time.perf_counter() - prompt_start
        ) * 1000

        observability_service.log_stage(
            "Prompt Builder",
            prompt_time,
        )

        # -------------------------------------------------------------
        # Step 13: Generate AI response
        # -------------------------------------------------------------
        response_generated = True
        llm_start = time.perf_counter()

        try:
            print("\n========== FINAL PROMPT ==========")
            print(prompt)
            print("==================================\n")

            answer = self.llm_service.generate_response(
                prompt
            )

            llm_time = (
                time.perf_counter() - llm_start
            ) * 1000

            observability_service.log_stage(
                "LLM",
                llm_time,
            )

        except Exception:

            response_generated = False

            llm_time = (
                time.perf_counter() - llm_start
            ) * 1000

            observability_service.log_stage(
                "LLM",
                llm_time,
            )

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

        # -------------------------------------------------------------
        # Step 15: Evaluation Logging
        # -------------------------------------------------------------
        similarities = [
            memory.get("similarity", 0.0)
            for memory in selected_memories
        ]

        importances = [
            memory.get("importance", 0.0)
            for memory in selected_memories
        ]

        context_scores = [
            memory.get("context_score", 0.0)
            for memory in selected_memories
        ]

        total_time = observability_service.end_trace(
            total_start
        )

        observability_service.log_stage(
            "Total Request",
            total_time,
        )

        EvaluationService.log_request(
            db=db,
            user_id=user_id,
            chat_session_id=session_id,
            query=question,
            retrieval_count=len(memories),
            selected_count=len(selected_memories),
            average_similarity=(
                sum(similarities) / len(similarities)
                if similarities else 0.0
            ),
            average_importance=(
                sum(importances) / len(importances)
                if importances else 0.0
            ),
            average_context_score=(
                sum(context_scores) / len(context_scores)
                if context_scores else 0.0
            ),
            precision_score=0.0,
            recall_score=0.0,
            response_generated=response_generated,
            response_length=len(answer),
            embedding_time_ms=0.0,
            retrieval_time_ms=retrieval_time,
            ranking_time_ms=0.0,
            context_time_ms=context_time,
            prompt_time_ms=prompt_time,
            llm_time_ms=llm_time,
            total_time_ms=total_time,
        )

        retrieval_analytics_service.log(
            db=db,
            user_id=user_id,
            chat_session_id=session_id,
            query=question,
            retrieved_count=len(memories),
            selected_count=len(selected_memories),
            average_similarity=(
                sum(similarities) / len(similarities)
                if similarities else 0.0
            ),
            retrieval_time_ms=retrieval_time,
        )

        system_metric_service.log(
            db=db,
            metric_name="llm_response_time",
            metric_value=llm_time,
            unit="ms",
        )

        system_metric_service.log(
            db=db,
            metric_name="retrieval_time",
            metric_value=retrieval_time,
            unit="ms",
        )

        system_metric_service.log(
            db=db,
            metric_name="total_request_time",
            metric_value=total_time,
            unit="ms",
        )

        return {
        "answer": answer,
        "retrieved_memories": selected_memories,
        "retrieved_documents": [
            {
                "document_id": chunk.document_id,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "similarity": round(
                    max(0.0, 1 - distance),
                    4,
                ),
            }
            for chunk, distance in document_chunks
        ],
    }