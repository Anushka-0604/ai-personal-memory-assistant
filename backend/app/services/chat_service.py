from sqlalchemy.orm import Session

from app.core.config import RAG_SIMILARITY_THRESHOLD
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
        question: str,
        top_k: int = 5,
    ):

        memories = search_memories(
            db=db,
            user_id=user_id,
            query=question,
            top_k=top_k,
        )

        # Keep only relevant memories
        filtered_memories = [
            memory
            for memory in memories
            if memory["similarity"] >= RAG_SIMILARITY_THRESHOLD
        ]

        memory_texts = [
            memory["content"]
            for memory in filtered_memories
        ]

        # No relevant memories found
        if not memory_texts:
            return {
                "answer": "I couldn't find any relevant memories to answer your question.",
                "retrieved_memories": [],
            }

        prompt = PromptBuilder.build_prompt(
            user_question=question,
            memories=memory_texts,
        )

        answer = self.llm_service.generate_response(prompt)

        return {
            "answer": answer,
            "retrieved_memories": filtered_memories,
        }