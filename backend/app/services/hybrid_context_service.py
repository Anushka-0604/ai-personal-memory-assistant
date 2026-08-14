from app.schemas.document_search import (
    DocumentSearchResult,
)


class HybridContextService:
    """
    Combines memories, documents, and knowledge graph
    information into one unified context.
    """

    def build_context(
        self,
        memories: list[str],
        documents: list[DocumentSearchResult],
        graph_context: list[dict] | None = None,
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

        # =====================================================
        # Knowledge Graph Section
        # =====================================================

        sections.append(
            "========== KNOWLEDGE GRAPH =========="
        )

        if graph_context:

            for connection in graph_context:

                subject = connection.get(
                    "subject"
                )

                relationship = connection.get(
                    "relationship"
                )

                object_entity = connection.get(
                    "object"
                )

                if (
                    subject
                    and relationship
                    and object_entity
                ):
                    sections.append(
                        f"- {subject} "
                        f"--[{relationship}]--> "
                        f"{object_entity}"
                    )

                else:

                    entity = connection.get(
                        "entity"
                    )

                    direction = connection.get(
                        "direction"
                    )

                    if (
                        entity
                        and direction
                        and relationship
                    ):
                        sections.append(
                            f"- {entity} "
                            f"({direction}) "
                            f"--[{relationship}]"
                        )

        else:

            sections.append(
                "No relevant knowledge graph connections."
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