import re


class RelationshipExtractionService:
    """
    Extracts high-confidence relationships between named entities.
    """

    # Only use reliable entity types for relationship extraction.
    ALLOWED_ENTITY_LABELS = {
        "PERSON",
        "ORG",
        "GPE",
        "LOC",
    }

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
        "connected_to": [
            "connected to",
            "connected with",
        ],
        "manages": [
            "manages",
            "manage",
        ],
        "stores": [
            "stores",
            "store",
        ],
        "maintains": [
            "maintains",
            "maintain",
        ],
        "compares_with": [
            "compares with",
            "compares them with",
            "compared with",
        ],
        "allows": [
            "allows",
            "allow",
        ],
        "supports": [
            "supports",
            "support",
        ],
        "retrieves": [
            "retrieves",
            "retrieve",
        ],
        "matches": [
            "matches",
            "match",
        ],
    }

    # Maximum number of characters allowed between
    # an entity and a relationship phrase.
    MAX_DISTANCE = 100

    def extract_relationships(
        self,
        text: str,
        entities: list[dict],
    ) -> list[dict]:

        if not text or not entities:
            return []

        relationships = []

        normalized_text = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        sentences = re.split(
            r"(?<=[.!?])\s+",
            normalized_text,
        )

        for sentence in sentences:

            sentence_lower = sentence.lower()

            sentence_entities = []

            for entity in entities:

                entity_text = entity.get(
                    "text",
                    "",
                ).strip()

                entity_label = entity.get("label")

                # Ignore unreliable entity types.
                if entity_label not in self.ALLOWED_ENTITY_LABELS:
                    continue

                if not entity_text:
                    continue

                position = sentence_lower.find(
                    entity_text.lower()
                )

                if position != -1:

                    sentence_entities.append(
                        (
                            position,
                            position + len(entity_text),
                            entity_text,
                        )
                    )

            if len(sentence_entities) < 2:
                continue

            sentence_entities.sort(
                key=lambda item: item[0]
            )

            for relationship_name, patterns in (
                self.RELATION_PATTERNS.items()
            ):

                for pattern in patterns:

                    for match in re.finditer(
                        re.escape(pattern.lower()),
                        sentence_lower,
                    ):

                        relation_start = match.start()
                        relation_end = match.end()

                        subject = self._find_subject(
                            sentence_entities,
                            relation_start,
                        )

                        object_entity = self._find_object(
                            sentence_entities,
                            relation_end,
                        )

                        if not subject or not object_entity:
                            continue

                        # Find the actual entity positions.
                        subject_position = next(
                            (
                                entity
                                for entity in sentence_entities
                                if entity[2] == subject
                                and entity[1] <= relation_start
                            ),
                            None,
                        )

                        object_position = next(
                            (
                                entity
                                for entity in sentence_entities
                                if entity[2] == object_entity
                                and entity[0] >= relation_end
                            ),
                            None,
                        )

                        if not subject_position or not object_position:
                            continue

                        # Reject relationships where entities
                        # are too far away from the relation.
                        subject_distance = (
                            relation_start
                            - subject_position[1]
                        )

                        object_distance = (
                            object_position[0]
                            - relation_end
                        )

                        if (
                            subject_distance
                            > self.MAX_DISTANCE
                        ):
                            continue

                        if (
                            object_distance
                            > self.MAX_DISTANCE
                        ):
                            continue

                        relationship = {
                            "subject": subject,
                            "relationship": relationship_name,
                            "object": object_entity,
                        }

                        if relationship not in relationships:
                            relationships.append(
                                relationship
                            )

        return relationships

    def _find_subject(
        self,
        entities: list[tuple],
        relation_start: int,
    ) -> str | None:

        candidates = [
            entity
            for entity in entities
            if entity[1] <= relation_start
        ]

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda item: item[1],
        )[2]

    def _find_object(
        self,
        entities: list[tuple],
        relation_end: int,
    ) -> str | None:

        candidates = [
            entity
            for entity in entities
            if entity[0] >= relation_end
        ]

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda item: item[0],
        )[2]


relationship_extraction_service = (
    RelationshipExtractionService()
)