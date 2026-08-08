class ClassificationService:
    """
    Classification service for memories and documents.
    """

    # =====================================================
    # MEMORY CLASSIFICATION
    # =====================================================

    CATEGORY_KEYWORDS = {
        "Work": [
            "meeting",
            "office",
            "project",
            "client",
            "job",
            "internship",
            "presentation",
            "conference",
            "company",
        ],
        "Education": [
            "exam",
            "assignment",
            "college",
            "class",
            "lecture",
            "study",
            "homework",
            "semester",
        ],
        "Health": [
            "doctor",
            "hospital",
            "medicine",
            "appointment",
            "exercise",
            "gym",
            "health",
        ],
        "Finance": [
            "salary",
            "bank",
            "payment",
            "invoice",
            "tax",
            "money",
            "investment",
        ],
        "Travel": [
            "flight",
            "trip",
            "hotel",
            "vacation",
            "airport",
            "travel",
        ],
        "Shopping": [
            "shopping",
            "buy",
            "bought",
            "order",
            "purchase",
            "groceries",
        ],
        "Relationships": [
            "friend",
            "family",
            "wife",
            "husband",
            "parents",
            "brother",
            "sister",
            "girlfriend",
            "boyfriend",
        ],
    }

    # =====================================================
    # DOCUMENT CLASSIFICATION
    # =====================================================

    DOCUMENT_CATEGORY_KEYWORDS = {
        "Academic": [
            "lecture",
            "course",
            "module",
            "university",
            "college",
            "semester",
            "syllabus",
            "curriculum",
            "subject",
            "chapter",
            "theory",
            "professor",
            "student",
        ],
        "Presentation": [
            "presentation",
            "slides",
            "slide",
            "ppt",
            "pptx",
            "powerpoint",
            "agenda",
            "conclusion",
        ],
        "Report": [
            "report",
            "executive summary",
            "introduction",
            "methodology",
            "results",
            "findings",
            "analysis",
            "recommendation",
        ],
        "Notes": [
            "notes",
            "lecture notes",
            "class notes",
            "summary",
            "revision",
            "important points",
        ],
        "Research": [
            "research",
            "abstract",
            "literature review",
            "experiment",
            "hypothesis",
            "dataset",
            "methodology",
            "references",
            "citation",
        ],
        "Assignment": [
            "assignment",
            "question",
            "problem statement",
            "submission",
            "task",
            "solution",
            "deadline",
        ],
        "Personal": [
            "personal",
            "diary",
            "journal",
            "my plans",
            "my goals",
            "my notes",
        ],
    }

    # =====================================================
    # MEMORY CLASSIFICATION
    # =====================================================

    def classify(self, text: str) -> str:
        """
        Classify a personal memory into a predefined category.
        """

        text = text.lower()

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return category

        return "Personal"

    # =====================================================
    # DOCUMENT CLASSIFICATION
    # =====================================================

    def classify_document(
        self,
        text: str,
        filename: str = "",
    ) -> str:
        """
        Classify an uploaded document.

        Classification is based on both:
        - document filename
        - extracted document text
        """

        combined_text = (
            f"{filename} {text}"
        ).lower()

        category_scores = {}

        for category, keywords in (
            self.DOCUMENT_CATEGORY_KEYWORDS.items()
        ):
            score = 0

            for keyword in keywords:
                if keyword in combined_text:
                    score += 1

            category_scores[category] = score

        # Find the category with the highest score
        best_category = max(
            category_scores,
            key=category_scores.get,
        )

        # If no keyword matched, classify as Other
        if category_scores[best_category] == 0:
            return "Other"

        return best_category


classification_service = ClassificationService()