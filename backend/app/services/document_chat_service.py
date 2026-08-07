from sqlalchemy.orm import Session

from app.services.document_prompt_builder import (
    DocumentPromptBuilder,
)
from app.services.document_rag_service import (
    document_rag_service,
)
from app.services.llm_service import (
    LLMService,
)


class DocumentChatService:
    """
    Handles document-based conversations.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def chat(
        self,
        db: Session,
        question: str,
        top_k: int = 5,
    ):
        # ------------------------------------------
        # Step 1: Retrieve document context
        # ------------------------------------------

        context = (
            document_rag_service.build_context(
                db=db,
                query=question,
                top_k=top_k,
            )
        )

        # ------------------------------------------
        # Step 2: Build prompt
        # ------------------------------------------

        prompt = (
            DocumentPromptBuilder.build_prompt(
                question=question,
                context=context,
            )
        )

        # ------------------------------------------
        # Step 3: Generate answer
        # ------------------------------------------

        answer = (
            self.llm_service.generate_response(
                prompt
            )
        )

        return {
            "answer": answer,
            "context": context,
        }


document_chat_service = (
    DocumentChatService()
)