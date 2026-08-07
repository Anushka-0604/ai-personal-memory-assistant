class HybridPromptBuilder:
    """
    Builds prompts for Hybrid RAG
    (Personal Memories + Documents).
    """

    SYSTEM_PROMPT = """
You are an AI Personal Memory & Decision Assistant.

You have access to two knowledge sources:

1. Personal memories
2. Uploaded documents

Rules:

1. Use both memories and documents whenever relevant.
2. Never invent information.
3. If the answer comes from a document,
   cite the document name and page number if available.
4. If the answer comes from memories,
   naturally incorporate that information.
5. If both sources support the answer,
   combine them into one coherent response.
6. If neither source contains the answer,
   clearly state that.
"""

    @staticmethod
    def build_prompt(
        question: str,
        context: str,
    ) -> str:

        return f"""
{HybridPromptBuilder.SYSTEM_PROMPT}

================ KNOWLEDGE ================

{context}

================ USER QUESTION ================

{question}

================ ASSISTANT RESPONSE ================
"""