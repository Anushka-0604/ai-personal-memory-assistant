import re

import spacy


class NERService:
    """
    Extracts meaningful named entities from document text using spaCy.

    Additional filtering is applied because technical PDFs and
    lecture slides often cause spaCy to classify headings,
    fragments, and technical terminology as named entities.
    """

    ALLOWED_LABELS = {
        "PERSON",
        "ORG",
        "GPE",
        "LOC",
        "FAC",
        "PRODUCT",
        "EVENT",
        "WORK_OF_ART",
    }

    # Generic technical terms that should not become
    # knowledge-graph entities.
    BLOCKED_TERMS = {
        "process",
        "process control block",
        "process state",
        "process priority",
        "process accounting information",
        "program counter",
        "cpu",
        "cpu registers",
        "register",
        "ram",
        "function",
        "current state",
        "unique id",
        "list of open files",
        "foreground/background",
        "context switch",
        "ready",
        "running",
        "suspended",
        "suspended ready",
        "suspended wait",
        "ready queue",
        "device",
        "backing store",
        "scheduling queues",
        "long term scheduler",
        "edition",
    }

    # Words that commonly appear in technical lecture slides
    # but are not useful named entities.
    TECHNICAL_WORDS = {
        "process",
        "processes",
        "state",
        "priority",
        "accounting",
        "information",
        "register",
        "registers",
        "program",
        "counter",
        "queue",
        "queues",
        "scheduler",
        "scheduling",
        "representation",
        "memory",
        "context",
        "switch",
        "current",
        "unique",
        "list",
        "files",
        "foreground",
        "background",
        "suspended",
        "ready",
        "running",
        "device",
        "pcb",
        "cpu",
        "ram",
        "edition",
        "diagram",
        "soln",
        "qna",
        "concept",
        "concepts",
        "system",
        "operation",
        "operations",
        "attribute",
        "attributes",
        "resource",
        "resources",
        "execution",
        "instruction",
        "instructions",
        "section",
        "chapter",
        "slide",
        "figure",
        "table",
        "job",
        "jobs",
    }

    # Common words that indicate an entity is probably
    # a sentence fragment rather than a real named entity.
    FRAGMENT_WORDS = {
        "the",
        "a",
        "an",
        "this",
        "that",
        "these",
        "those",
        "each",
        "every",
        "when",
        "where",
        "which",
        "whose",
        "and",
        "or",
        "of",
        "to",
        "for",
        "from",
        "with",
        "by",
        "in",
        "on",
        "is",
        "are",
        "was",
        "were",
    }

    MINIMUM_LENGTH_BY_LABEL = {
        "PERSON": 2,
        "ORG": 2,
        "GPE": 2,
        "LOC": 2,
        "FAC": 3,
        "PRODUCT": 3,
        "EVENT": 4,
        "WORK_OF_ART": 4,
    }

    def __init__(self):
        self.nlp = spacy.load(
            "en_core_web_sm"
        )

    # =====================================================
    # Main Extraction
    # =====================================================

    def extract_entities(
        self,
        text: str,
    ) -> list[dict]:
        """
        Extract meaningful named entities from text.
        """

        if not text or not text.strip():
            return []

        doc = self.nlp(text)

        entities = []
        seen = set()

        for entity in doc.ents:

            entity_text = self._clean_entity_text(
                entity.text
            )

            label = entity.label_

            # ---------------------------------------------
            # Allowed labels
            # ---------------------------------------------

            if label not in self.ALLOWED_LABELS:
                continue

            if not entity_text:
                continue

            # ---------------------------------------------
            # Must contain alphabetic characters
            # ---------------------------------------------

            if not re.search(
                r"[A-Za-z]",
                entity_text,
            ):
                continue

            # ---------------------------------------------
            # Minimum length
            # ---------------------------------------------

            minimum_length = (
                self.MINIMUM_LENGTH_BY_LABEL.get(
                    label,
                    2,
                )
            )

            if len(entity_text) < minimum_length:
                continue

            normalized_text = (
                self._normalize_for_comparison(
                    entity_text
                )
            )

            # ---------------------------------------------
            # Exact blocked terms
            # ---------------------------------------------

            if normalized_text in self.BLOCKED_TERMS:
                continue

            # ---------------------------------------------
            # PDF fragment detection
            # ---------------------------------------------

            if self._looks_like_pdf_fragment(
                entity_text
            ):
                continue

            # ---------------------------------------------
            # Technical heading detection
            # ---------------------------------------------

            if self._looks_like_technical_heading(
                entity_text
            ):
                continue

            # ---------------------------------------------
            # Sentence fragment detection
            # ---------------------------------------------

            if self._looks_like_sentence_fragment(
                entity_text
            ):
                continue

            # ---------------------------------------------
            # Suspicious entity labels
            # ---------------------------------------------

            if self._looks_like_false_positive(
                entity_text,
                label,
            ):
                continue

            # ---------------------------------------------
            # Duplicate removal
            # ---------------------------------------------

            key = (
                normalized_text,
                label,
            )

            if key in seen:
                continue

            seen.add(key)

            entities.append(
                {
                    "text": entity_text,
                    "label": label,
                    "description": spacy.explain(
                        label
                    ),
                }
            )

        return entities

    # =====================================================
    # Text Cleaning
    # =====================================================

    @staticmethod
    def _clean_entity_text(
        entity_text: str,
    ) -> str:
        """
        Clean whitespace and common PDF artifacts.
        """

        entity_text = re.sub(
            r"\s+",
            " ",
            entity_text,
        ).strip()

        entity_text = entity_text.strip(
            " \t\r\n.,;:!?-–—•"
        )

        return entity_text

    # =====================================================
    # Normalization
    # =====================================================

    @staticmethod
    def _normalize_for_comparison(
        entity_text: str,
    ) -> str:
        """
        Normalize entity text for comparisons.
        """

        normalized = entity_text.lower()

        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        ).strip()

        return normalized

    # =====================================================
    # PDF Fragment Detection
    # =====================================================

    @staticmethod
    def _looks_like_pdf_fragment(
        entity_text: str,
    ) -> bool:
        """
        Detect fragments commonly produced by PDF extraction.
        """

        words = entity_text.split()

        # Very long entity spans are suspicious.
        if len(words) > 6:
            return True

        # Slide/page numbering artifacts.
        if re.search(
            r"\b\d+\.\d+\b",
            entity_text,
        ):
            return True

        # Common PDF artifacts.
        suspicious_markers = [
            "",
            "",
            "•",
            "",
            "ï®",
            "ï‚§",
            "â€¢",
            "ïƒ",
            ":-",
        ]

        if any(
            marker in entity_text
            for marker in suspicious_markers
        ):
            return True

        return False

    # =====================================================
    # Technical Heading Detection
    # =====================================================

    @classmethod
    def _looks_like_technical_heading(
        cls,
        entity_text: str,
    ) -> bool:
        """
        Reject technical lecture-slide headings and phrases.
        """

        normalized = cls._normalize_for_comparison(
            entity_text
        )

        words = normalized.split()

        if not words:
            return True

        technical_count = sum(
            word in cls.TECHNICAL_WORDS
            for word in words
        )

        # If every word is technical terminology,
        # this is almost certainly not a real entity.
        if technical_count == len(words):
            return True

        # If most words are technical terminology,
        # reject the entity.
        if (
            len(words) >= 2
            and technical_count / len(words)
            >= 0.60
        ):
            return True

        # Explicit heading patterns.
        heading_patterns = [
            r"^the\s+process",
            r"^process\s+priority",
            r"^process\s+accounting",
            r"^scheduling\s+queues",
            r"^edition\s+",
            r"^diagram\s+of",
            r"^representation\s+of",
            r"^qna\s+",
        ]

        for pattern in heading_patterns:

            if re.search(
                pattern,
                normalized,
            ):
                return True

        return False

    # =====================================================
    # Sentence Fragment Detection
    # =====================================================

    @classmethod
    def _looks_like_sentence_fragment(
        cls,
        entity_text: str,
    ) -> bool:
        """
        Reject entities that look like pieces of sentences.
        """

        normalized = cls._normalize_for_comparison(
            entity_text
        )

        words = normalized.split()

        if not words:
            return True

        # A multi-word entity beginning with common
        # sentence words is suspicious.
        if (
            len(words) >= 3
            and words[0] in cls.FRAGMENT_WORDS
        ):
            return True

        # A multi-word entity ending in common grammatical
        # words is suspicious.
        if (
            len(words) >= 3
            and words[-1] in cls.FRAGMENT_WORDS
        ):
            return True

        return False

    # =====================================================
    # False Positive Detection
    # =====================================================

    @classmethod
    def _looks_like_false_positive(
        cls,
        entity_text: str,
        label: str,
    ) -> bool:
        """
        Additional protection against obvious spaCy
        false positives in technical documents.
        """

        normalized = cls._normalize_for_comparison(
            entity_text
        )

        words = normalized.split()

        # A single generic technical word should not
        # become a named entity.
        if (
            len(words) == 1
            and words[0] in cls.TECHNICAL_WORDS
        ):
            return True

        # PERSON entities should normally be short,
        # name-like phrases. Long technical phrases are
        # almost certainly false positives.
        if label == "PERSON":

            if len(words) > 4:
                return True

            if any(
                word in cls.TECHNICAL_WORDS
                for word in words
            ):
                return True

        # GPE/LOC should not be obvious technical terms.
        if label in {
            "GPE",
            "LOC",
        }:

            if any(
                word in cls.TECHNICAL_WORDS
                for word in words
            ):
                return True

        return False


ner_service = NERService()