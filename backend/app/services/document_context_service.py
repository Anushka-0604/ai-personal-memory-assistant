from app.schemas.document_search import (
    DocumentSearchResult,
)


class DocumentContextService:
    """
    Builds the final context sent to the LLM
    from retrieved document chunks.
    """

    def build_context(
        self,
        results: list[DocumentSearchResult],
        max_chunks: int = 5,
    ) -> str:

        context = []

        for result in results[:max_chunks]:

            context.append(
                f"[Document: {result.document_name}]"
            )

            context.append(
                f"[Chunk: {result.chunk_index}]"
            )

            context.append(result.content)

            context.append("")

        return "\n".join(context)


document_context_service = (
    DocumentContextService()
)