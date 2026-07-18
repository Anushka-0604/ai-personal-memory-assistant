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

You are having an ongoing conversation with the user.

Use BOTH the previous conversation and the relevant memories to answer naturally.

If the answer cannot be found in either the conversation or the memories, clearly say that you could not find relevant information.

Previous Conversation:
{history_section}

Relevant Memories:
{memory_context}

Current User Question:
{user_question}

Answer:
"""

        return prompt.strip()