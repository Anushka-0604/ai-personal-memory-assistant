class ContextSelector:

    CATEGORY_BOOSTS = {
        "Work": 0.10,
        "Personal": 0.08,
        "Health": 0.08,
        "Education": 0.08,
        "Finance": 0.08,
        "Travel": 0.06,
        "Preference": 0.05,
        "General": 0.00,
    }

    def select(
        self,
        memories,
        similarity_threshold=0.50,
        max_memories=5,
    ):
        filtered = [
            memory
            for memory in memories
            if memory["similarity"] >= similarity_threshold
        ]

        for memory in filtered:

            category_boost = self.CATEGORY_BOOSTS.get(
                memory["category"],
                0.0,
            )

            memory["context_score"] = (
                memory["similarity"] * 0.50
                + memory["importance_score"] * 0.25
                + memory["recency_score"] * 0.15
                + category_boost * 0.10
            )

        filtered.sort(
            key=lambda x: x["context_score"],
            reverse=True,
        )

        return filtered[:max_memories]


context_selector = ContextSelector()