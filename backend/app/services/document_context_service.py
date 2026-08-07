from app.schemas.document_search import (
    DocumentSearchResult,
)


class DocumentContextService:
    """
    Builds the final context sent to the LLM
    together with document citations.
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

            if hasattr(result, "page_number") and result.page_number is not None:
                context.append(
                    f"[Page: {result.page_number}]"
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