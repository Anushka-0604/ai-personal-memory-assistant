from app.schemas.document_search import (
    DocumentSearchResult,
)


class HybridContextService:
    """
    Combines memories and documents into
    one unified context.
    """

    def build_context(
        self,
        memories: list[str],
        documents: list[DocumentSearchResult],
    ) -> str:

        sections = []

        # =====================================================
        # Memory Section
        # =====================================================

        sections.append(
            "========== MEMORIES =========="
        )

        if memories:

            for memory in memories:
                sections.append(
                    f"- {memory}"
                )

        else:

            sections.append(
                "No relevant memories."
            )

        sections.append("")

        # =====================================================
        # Document Section
        # =====================================================

        sections.append(
            "========== DOCUMENTS =========="
        )

        if documents:

            for document in documents:

                sections.append(
                    f"[Document: {document.document_name}]"
                )

                sections.append(
                    document.content
                )

                sections.append("")

        else:

            sections.append(
                "No relevant documents."
            )

        return "\n".join(
            sections
        )


# =====================================================
# Singleton Service
# =====================================================

hybrid_context_service = (
    HybridContextService()
)