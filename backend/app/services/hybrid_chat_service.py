from sqlalchemy.orm import Session

from app.services.hybrid_context_service import (
    hybrid_context_service,
)
from app.services.hybrid_prompt_builder import (
    HybridPromptBuilder,
)
from app.services.llm_service import (
    LLMService,
)
from app.services.memory_service import (
    search_memories,
)
from app.services.document_search_service import (
    semantic_document_search,
)
from app.services.graph_query_service import (
    graph_query_service,
)


class HybridChatService:
    """
    Hybrid Retrieval-Augmented Generation.

    Searches:
    - Personal memories
    - Uploaded documents
    - Knowledge graph

    and combines them into one unified response.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def chat(
        self,
        db: Session,
        user_id: int,
        question: str,
        top_k: int = 5,
    ):

        # -----------------------------------------
        # Retrieve memories
        # -----------------------------------------

        memories = search_memories(
            db=db,
            user_id=user_id,
            query=question,
            top_k=top_k,
        )

        memory_texts = [
            memory["content"]
            for memory in memories
        ]

        # -----------------------------------------
        # Retrieve documents
        # -----------------------------------------

        documents = semantic_document_search(
            db=db,
            query=question,
            top_k=top_k,
        )

        # -----------------------------------------
        # Retrieve Knowledge Graph connections
        # -----------------------------------------

        graph_context = []

        try:
            graph_context = (
                graph_query_service.get_entity_connections(
                    question
                )
            )

        except Exception:
            graph_context = []

        # -----------------------------------------
        # Build unified context
        # -----------------------------------------

        context = (
            hybrid_context_service.build_context(
                memories=memory_texts,
                documents=documents,
                graph_context=graph_context,
            )
        )

        # -----------------------------------------
        # Build prompt
        # -----------------------------------------

        prompt = (
            HybridPromptBuilder.build_prompt(
                question=question,
                context=context,
            )
        )

        # -----------------------------------------
        # Generate answer
        # -----------------------------------------

        answer = (
            self.llm_service.generate_response(
                prompt
            )
        )

        return {
            "answer": answer,
            "context": context,
            "memory_count": len(memories),
            "document_count": len(documents),
            "graph_count": len(graph_context),
        }


# =====================================================
# Singleton Service
# =====================================================

hybrid_chat_service = (
    HybridChatService()
)