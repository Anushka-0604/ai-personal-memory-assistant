class PromptBuilder:
    """
    Responsible for constructing prompts for the LLM.
    """

    @staticmethod
    def build_prompt(user_question: str, memories: list[str]) -> str:
        """
        Builds a prompt using the user's question and retrieved memories.
        """

        memory_context = "\n".join(
            f"- {memory}" for memory in memories
        )

        prompt = f"""
You are an AI Personal Memory & Decision Assistant.

Your job is to answer the user's question ONLY using the memories provided below.

If the answer is not present in the memories, clearly say that you could not find relevant information.

Relevant Memories:
{memory_context}

User Question:
{user_question}

Answer:
"""

        return prompt.strip()