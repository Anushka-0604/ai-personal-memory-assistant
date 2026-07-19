from app.services.reference_resolution_service import (
    ReferenceResolutionService,
)


class PromptBuilder:
    """
    Responsible for constructing prompts for the LLM.
    """

    @staticmethod
    def build_prompt(
        user_question: str,
        memories: list[str],
        conversation_history: str = "",
    ) -> str:
        """
        Builds a prompt using the user's question,
        previous conversation history, and retrieved memories.
        """

        # Placeholder for future reference resolution.
        # In later steps, we'll pass the actual conversation
        # history objects to this service.
        resolved_question = (
            ReferenceResolutionService.resolve_reference(
                question=user_question,
                conversation_history=[],
            )
        )

        memory_context = "\n".join(
            f"- {memory}" for memory in memories
        )

        history_section = (
            conversation_history
            if conversation_history
            else "No previous conversation."
        )

        prompt = f"""
You are an AI Personal Memory & Decision Assistant.

Your role is to help the user by answering questions using their stored memories and the ongoing conversation.

Instructions:
- Use the retrieved memories as the primary source of information.
- Use the previous conversation only to understand the context.
- Do not invent, assume, or fabricate information that is not present in the memories or conversation.
- If the required information is unavailable, clearly state that you could not find relevant information.
- Provide clear, accurate, and concise answers in a natural conversational tone.

Previous Conversation:
{history_section}

Relevant Memories:
{memory_context}

Current User Question:
{resolved_question}

Answer:
"""

        return prompt.strip()