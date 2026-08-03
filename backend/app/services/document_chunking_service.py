class DocumentChunkingService:

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
    ) -> list[str]:

        if not text.strip():
            return []

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunks.append(
                text[start:end].strip()
            )

            start = end

        return chunks


document_chunking_service = (
    DocumentChunkingService()
)