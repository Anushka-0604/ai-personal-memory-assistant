import re


class DocumentChunkingService:

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
    ) -> list[str]:
        """
        Intelligent paragraph-aware chunking.

        Large paragraphs are further split into
        fixed-size chunks.
        """

        if not text.strip():
            return []

        paragraphs = self._split_paragraphs(
            text
        )

        chunks = []

        for paragraph in paragraphs:

            if len(paragraph) <= chunk_size:

                chunks.append(paragraph)

                continue

            start = 0

            while start < len(paragraph):

                end = start + chunk_size

                chunks.append(
                    paragraph[start:end].strip()
                )

                start = end

        return chunks

    def _split_paragraphs(
        self,
        text: str,
    ) -> list[str]:
        """
        Split text into paragraphs.

        Multiple blank lines are treated as
        paragraph separators.
        """

        paragraphs = re.split(
            r"\n\s*\n",
            text,
        )

        return [
            paragraph.strip()
            for paragraph in paragraphs
            if paragraph.strip()
        ]


document_chunking_service = (
    DocumentChunkingService()
)