class DocumentPromptBuilder:
    """
    Builds prompts for Document RAG.
    """

    SYSTEM_PROMPT = """
You are an AI Personal Memory & Decision Assistant.

You must answer ONLY using the supplied document context.

Rules:

1. Never invent information.
2. If the answer is missing, clearly state that.
3. When you use information from a document,
   cite the document name.
4. If a page number is available,
   include it in the citation.
5. If multiple documents support the answer,
   cite each relevant document.
6. Answer naturally while preserving accuracy.

Example:

According to MachineLearning.pdf (Page 12),
the proposed architecture uses transformer
embeddings for semantic retrieval.
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