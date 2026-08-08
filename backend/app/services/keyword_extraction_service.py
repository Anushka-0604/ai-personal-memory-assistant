import re
from collections import Counter


class KeywordExtractionService:
    """
    Extracts important keywords from document text.
    """

    STOPWORDS = {
        "the",
        "and",
        "for",
        "that",
        "this",
        "with",
        "from",
        "are",
        "was",
        "were",
        "have",
        "has",
        "had",
        "will",
        "would",
        "could",
        "should",
        "about",
        "into",
        "their",
        "there",
        "which",
        "when",
        "where",
        "what",
        "who",
        "how",
        "why",
        "you",
        "your",
        "they",
        "them",
        "our",
        "out",
        "not",
        "but",
        "can",
        "may",
        "also",
        "than",
        "then",
        "these",
        "those",
        "been",
        "being",
        "its",
        "it's",
        "all",
        "any",
        "some",
        "such",
        "more",
        "most",
        "other",
        "only",
        "very",
        "each",
        "both",
        "between",
        "through",
        "during",
        "over",
        "under",
        "using",
        "used",
        "use",
        "based",
        "following",
        "information",
    }

    def extract_keywords(
        self,
        text: str,
        top_k: int = 10,
    ) -> list[str]:
        """
        Extract the most frequent meaningful keywords.
        """

        if not text:
            return []

        # Convert text to lowercase
        text = text.lower()

        # Extract alphabetic words
        words = re.findall(
            r"\b[a-zA-Z][a-zA-Z-]{2,}\b",
            text,
        )

        # Remove stopwords
        filtered_words = [
            word
            for word in words
            if word not in self.STOPWORDS
        ]

        # Count word frequency
        word_counts = Counter(
            filtered_words
        )

        # Select most frequent keywords
        keywords = [
            word
            for word, _ in word_counts.most_common(
                top_k
            )
        ]

        return keywords


keyword_extraction_service = (
    KeywordExtractionService()
)