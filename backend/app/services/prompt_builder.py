class PromptBuilder:
    """
    Responsible for constructing prompts for the LLM.
    """

    @staticmethod
    def build_prompt(
        user_question: str,
        context: str,
    ) -> str:
        """
        Builds the final prompt using the
        unified conversation context.
        """

        prompt = f"""
You are an AI Personal Memory & Decision Assistant.

Your role is to help the user by answering questions using the provided context.

Instructions:
- Use ONLY the information present in the context.
- Do not invent, assume, or fabricate information.
- If the answer cannot be found in the context, clearly say so.
- Answer naturally and concisely.

Context:
{context}

Current User Question:
{user_question}

Answer:
"""

        return prompt.strip()