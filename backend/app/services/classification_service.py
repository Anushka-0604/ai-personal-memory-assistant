class ClassificationService:
    """Classifies memories into predefined categories."""

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

    def classify(self, text: str) -> str:
        text = text.lower()

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return category

        return "Personal"


classification_service = ClassificationService()