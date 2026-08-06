import math
import re

from app.schemas.document_chunk import (
    DocumentChunkMetadata,
)


class DocumentChunkingService:

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
        overlap_sentences: int | None = None,
    ) -> list[str]:
        """
        Backward-compatible chunking.
        Returns only chunk text.
        """

        metadata_chunks = self.chunk_text_with_metadata(
            text=text,
            document_id=0,
            chunk_size=chunk_size,
            overlap_sentences=overlap_sentences,
        )

        return [
            chunk.content
            for chunk in metadata_chunks
        ]

    def chunk_text_with_metadata(
        self,
        text: str,
        document_id: int,
        chunk_size: int = 500,
        overlap_sentences: int | None = None,
    ) -> list[DocumentChunkMetadata]:
        """
        Intelligent chunking with metadata.
        """

        if not text.strip():
            return []

        paragraphs = self._split_paragraphs(text)

        chunks = []

        chunk_index = 0

        for paragraph_index, paragraph in enumerate(
            paragraphs
        ):

            if len(paragraph) <= chunk_size:

                chunks.append(
                    DocumentChunkMetadata(
                        document_id=document_id,
                        chunk_index=chunk_index,
                        paragraph_index=paragraph_index,
                        sentence_count=len(
                            self._split_sentences(
                                paragraph
                            )
                        ),
                        character_count=len(
                            paragraph
                        ),
                        content=paragraph,
                    )
                )

                chunk_index += 1

                continue

            paragraph_chunks = (
                self._split_large_paragraph(
                    paragraph,
                    chunk_size,
                    overlap_sentences,
                )
            )

            for chunk in paragraph_chunks:

                chunks.append(
                    DocumentChunkMetadata(
                        document_id=document_id,
                        chunk_index=chunk_index,
                        paragraph_index=paragraph_index,
                        sentence_count=len(
                            self._split_sentences(
                                chunk
                            )
                        ),
                        character_count=len(
                            chunk
                        ),
                        content=chunk,
                    )
                )

                chunk_index += 1

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

    def _split_sentences(
        self,
        text: str,
    ) -> list[str]:

        return [
            sentence.strip()
            for sentence in re.split(
                r"(?<=[.!?])\s+",
                text,
            )
            if sentence.strip()
        ]

    def _split_large_paragraph(
        self,
        paragraph: str,
        chunk_size: int,
        overlap_sentences: int | None,
    ) -> list[str]:

        sentences = self._split_sentences(
            paragraph
        )

        if overlap_sentences is None:
            overlap_sentences = (
                self._calculate_overlap(
                    len(sentences)
                )
            )

        chunks = []

        current_chunk = []
        current_length = 0

        for sentence in sentences:

            sentence_length = len(sentence)

            if (
                current_length + sentence_length
                <= chunk_size
            ):
                current_chunk.append(sentence)
                current_length += (
                    sentence_length + 1
                )

            else:

                if current_chunk:
                    chunks.append(
                        " ".join(current_chunk)
                    )

                overlap = (
                    current_chunk[
                        -overlap_sentences:
                    ]
                    if overlap_sentences > 0
                    else []
                )

                current_chunk = overlap + [
                    sentence
                ]

                current_length = sum(
                    len(s) + 1
                    for s in current_chunk
                )

        if current_chunk:
            chunks.append(
                " ".join(current_chunk)
            )

        return chunks

    def _calculate_overlap(
        self,
        total_sentences: int,
    ) -> int:

        return max(
            1,
            min(
                3,
                math.ceil(
                    total_sentences * 0.10
                ),
            ),
        )


document_chunking_service = (
    DocumentChunkingService()
)