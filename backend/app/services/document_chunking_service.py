import re


class DocumentChunkingService:

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
    ) -> list[str]:
        """
        Paragraph-aware and sentence-aware chunking.
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

            chunks.extend(
                self._split_large_paragraph(
                    paragraph,
                    chunk_size,
                )
            )

        return chunks

    def _split_paragraphs(
        self,
        text: str,
    ) -> list[str]:

        paragraphs = re.split(
            r"\n\s*\n",
            text,
        )

        return [
            paragraph.strip()
            for paragraph in paragraphs
            if paragraph.strip()
        ]

    def _split_large_paragraph(
        self,
        paragraph: str,
        chunk_size: int,
    ) -> list[str]:
        """
        Split large paragraphs at sentence boundaries.
        """

        sentences = re.split(
            r"(?<=[.!?])\s+",
            paragraph,
        )

        chunks = []

        current_chunk = ""

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            candidate = (
                current_chunk + " " + sentence
            ).strip()

            if (
                len(candidate)
                <= chunk_size
            ):
                current_chunk = candidate

            else:

                if current_chunk:
                    chunks.append(
                        current_chunk
                    )

                current_chunk = sentence

        if current_chunk:
            chunks.append(
                current_chunk
            )

        return chunks


document_chunking_service = (
    DocumentChunkingService()
)