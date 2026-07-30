class QueryRewriteService:
    """
    Rewrites short or ambiguous user queries into
    richer search queries for hybrid retrieval.
    """

    def __init__(self):
        self.query_map = {
            "meeting": [
                "meeting",
                "appointment",
                "project",
                "schedule",
                "work",
            ],
            "interview": [
                "interview",
                "job",
                "career",
                "hiring",
                "recruiter",
            ],
            "exam": [
                "exam",
                "test",
                "education",
                "university",
                "assessment",
            ],
            "google": [
                "google",
                "organization",
                "company",
                "work",
            ],
            "travel": [
                "travel",
                "trip",
                "vacation",
                "journey",
            ],
            "doctor": [
                "doctor",
                "hospital",
                "medical",
                "health",
            ],
        }

    def rewrite(self, query: str) -> str:
        words = query.lower().split()

        expanded = []

        for word in words:
            if word in self.query_map:
                expanded.extend(
                    self.query_map[word]
                )
            else:
                expanded.append(word)

        return " ".join(
            dict.fromkeys(expanded)
        )


query_rewrite_service = QueryRewriteService()