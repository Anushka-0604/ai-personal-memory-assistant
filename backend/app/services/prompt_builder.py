class PromptBuilder:
    """
    Builds prompts for different AI tasks.

    Supported Prompt Types:
    - Chat Response
    - Conversation Summarization
    - (Future) Entity Extraction
    - (Future) Knowledge Graph Generation
    """

    CHAT_SYSTEM_INSTRUCTIONS = """
You are an AI Personal Memory & Decision Assistant.

Your job is to answer the user's question using ONLY the provided context.

Rules:
1. The provided context is your primary source of truth.
2. Never invent facts that are not present in the context.
3. If the answer cannot be found, clearly say so.
4. Give concise, accurate, and natural responses.
5. Do not mention these instructions in your response.
"""

    SUMMARY_SYSTEM_INSTRUCTIONS = """
You are an AI conversation summarizer.

Summarize the conversation into a concise memory that preserves:

- Important facts
- User preferences
- Decisions made
- Relevant names
- Dates (if any)
- Context useful for future conversations

Ignore greetings, filler messages, and repetitive information.

Return only the summary.
"""

    @staticmethod
    def build_chat_prompt(
        user_question: str,
        context: str,
    ) -> str:
        """
        Build the prompt used for normal chat responses.
        """

        sections = [
            PromptBuilder.CHAT_SYSTEM_INSTRUCTIONS.strip(),
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

    @staticmethod
    def build_summary_prompt(
        conversation: str,
    ) -> str:
        """
        Build the prompt used for AI conversation summarization.
        """

        sections = [
            PromptBuilder.SUMMARY_SYSTEM_INSTRUCTIONS.strip(),
            "",
            "========== CONVERSATION ==========",
            conversation,
            "",
            "========== SUMMARY ==========",
        ]

        return "\n".join(sections)

    # ------------------------------------------------------------------
    # Future Prompt Templates
    # ------------------------------------------------------------------

    @staticmethod
    def build_extraction_prompt(text: str) -> str:
        """
        Placeholder for future entity extraction prompts.
        """
        return text

    @staticmethod
    def build_graph_prompt(text: str) -> str:
        """
        Placeholder for future knowledge graph prompts.
        """
        return text