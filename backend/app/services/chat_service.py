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
        # Retrieve relevant memories
        memories = search_memories(
            db=db,
            user_id=user_id,
            query=question,
            top_k=top_k,
        )

        # Keep only memories above the similarity threshold
        filtered_memories = [
            memory
            for memory in memories
            if memory["similarity"] >= RAG_SIMILARITY_THRESHOLD
        ]

        # If no relevant memories are found, return immediately
        if not filtered_memories:
            return {
                "answer": (
                    "I couldn't find any relevant memories "
                    "to answer your question."
                ),
                "retrieved_memories": [],
            }

        # Extract memory texts for prompt construction
        memory_texts = [
            memory["content"]
            for memory in filtered_memories
        ]

        # Build the RAG prompt
        prompt = PromptBuilder.build_prompt(
            user_question=question,
            memories=memory_texts,
        )

        # Generate response from the LLM
        answer = self.llm_service.generate_response(prompt)

        return {
            "answer": answer,
            "retrieved_memories": filtered_memories,
        }