class PromptBuilder:
    """
    Builds structured prompts for the LLM.
    """

    SYSTEM_INSTRUCTIONS = """
You are an AI Personal Memory & Decision Assistant.

You help users answer questions using only the provided context.

Rules:
1. Use the context as your primary source of truth.
2. Never invent information.
3. If the answer is unavailable, clearly state that you could not find it.
4. Be concise, accurate, and natural.
"""

    @staticmethod
    def build_prompt(
        user_question: str,
        context: str,
    ) -> str:
        """
        Construct the final prompt.
        """

        sections = [
            PromptBuilder.SYSTEM_INSTRUCTIONS.strip(),
            "",
            "========== CONTEXT ==========",
            context,
            "",
            "========== USER QUESTION ==========",
            user_question,
            "",
            "========== ASSISTANT RESPONSE ==========",
        ]

        return "\n".join(sections)