class RelationshipExtractionService:
    """
    Extracts simple relationships between named entities
    using lightweight rule-based patterns.
    """

    RELATION_PATTERNS = {
        "works_at": [
            "works at",
            "working at",
            "works for",
            "employed at",
            "employed by",
        ],
        "studies_at": [
            "studies at",
            "studying at",
            "student at",
        ],
        "located_in": [
            "located in",
            "based in",
            "situated in",
        ],
        "teaches": [
            "teaches",
            "teaching",
            "professor of",
        ],
        "works_on": [
            "works on",
            "working on",
            "developed",
            "developing",
            "project on",
        ],
        "part_of": [
            "part of",
            "belongs to",
            "member of",
        ],
    }

    def extract_relationships(
        self,
        text: str,
        entities: list[dict],
    ) -> list[dict]:
        """
        Extract relationships between entities using
        predefined textual patterns.
        """

        if not text or not entities:
            return []

        relationships = []
        text_lower = text.lower()

        for pattern_name, patterns in self.RELATION_PATTERNS.items():
            for pattern in patterns:
                start = 0

                while True:
                    position = text_lower.find(pattern, start)

                    if position == -1:
                        break

                    before = text[:position].strip()
                    after = text[
                        position + len(pattern):
                    ].strip()

                    subject = self._find_nearest_entity(
                        before,
                        entities,
                        from_end=True,
                    )

                    object_entity = self._find_nearest_entity(
                        after,
                        entities,
                        from_end=False,
                    )

                    if (
                        subject
                        and object_entity
                        and subject != object_entity
                    ):
                        relationship = {
                            "subject": subject,
                            "relationship": pattern_name,
                            "object": object_entity,
                        }

                        if relationship not in relationships:
                            relationships.append(
                                relationship
                            )

                    start = position + len(pattern)

        return relationships

    def _find_nearest_entity(
        self,
        text: str,
        entities: list[dict],
        from_end: bool,
    ) -> str | None:
        """
        Find the nearest known entity in a piece of text.
        """

        candidates = []

        for entity in entities:
            entity_text = entity.get("text")

            if not entity_text:
                continue

            position = text.lower().rfind(
                entity_text.lower()
            )

            if not from_end:
                position = text.lower().find(
                    entity_text.lower()
                )

            if position != -1:
                candidates.append(
                    (position, entity_text)
                )

        if not candidates:
            return None

        if from_end:
            return max(
                candidates,
                key=lambda item: item[0],
            )[1]

        return min(
            candidates,
            key=lambda item: item[0],
        )[1]


relationship_extraction_service = (
    RelationshipExtractionService()
)