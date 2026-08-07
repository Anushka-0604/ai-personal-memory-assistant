class DocumentPromptBuilder:
    """
    Builds prompts for Document RAG.
    """

    SYSTEM_PROMPT = """
You are an AI Personal Memory & Decision Assistant.

You must answer the user's question ONLY using the provided document context.

Rules:

1. Use only the supplied document context.
2. Do not invent facts.
3. If the answer is not present, clearly say you cannot find it.
4. Answer naturally and clearly.
5. Cite the document whenever possible.
"""

    @staticmethod
    def build_prompt(
        question: str,
        context: str,
    ) -> str:

        return f"""
{DocumentPromptBuilder.SYSTEM_PROMPT}

================ DOCUMENT CONTEXT ================

{context}

================ USER QUESTION ================

{question}

================ ANSWER ================
"""