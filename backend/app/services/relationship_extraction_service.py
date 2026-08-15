import re


class RelationshipExtractionService:
    """
    Extracts high-confidence relationships between named entities.

    Relationships are extracted only when:
    - the relationship phrase occurs inside a sentence,
    - the entities are reasonably close to the phrase,
    - the entity types are compatible with that relationship,
    - and the relationship is not obviously caused by technical
      document/PDF wording.
    """

    ALLOWED_ENTITY_LABELS = {
        "PERSON",
        "ORG",
        "GPE",
        "LOC",
        "EVENT",
        "PRODUCT",
        "WORK_OF_ART",
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

    # Keep the relationship phrase close to both entities.
    MAX_DISTANCE = 80

    # Relationship -> valid (subject label, object label) pairs.
    RELATION_ENTITY_TYPES = {
        "works_at": {
            ("PERSON", "ORG"),
        },
        "studies_at": {
            ("PERSON", "ORG"),
        },
        "located_in": {
            ("PERSON", "GPE"),
            ("PERSON", "LOC"),
            ("ORG", "GPE"),
            ("ORG", "LOC"),
        },
        "teaches": {
            ("PERSON", "ORG"),
            ("PERSON", "PERSON"),
        },
        "works_on": {
            ("PERSON", "ORG"),
            ("PERSON", "PRODUCT"),
            ("PERSON", "EVENT"),
            ("ORG", "ORG"),
            ("ORG", "PRODUCT"),
            ("ORG", "EVENT"),
        },
        "part_of": {
            ("PERSON", "ORG"),
            ("ORG", "ORG"),
            ("PRODUCT", "ORG"),
            ("EVENT", "ORG"),
        },
        "connected_to": {
            ("PERSON", "PERSON"),
            ("PERSON", "ORG"),
            ("ORG", "PERSON"),
            ("ORG", "ORG"),
            ("ORG", "GPE"),
            ("ORG", "LOC"),
            ("GPE", "ORG"),
            ("LOC", "ORG"),
        },
        "manages": {
            ("PERSON", "ORG"),
            ("PERSON", "PERSON"),
            ("ORG", "ORG"),
        },
        "stores": {
            ("ORG", "PRODUCT"),
            ("ORG", "ORG"),
        },
        "maintains": {
            ("PERSON", "ORG"),
            ("ORG", "ORG"),
            ("ORG", "PRODUCT"),
        },
        "compares_with": {
            ("PERSON", "PERSON"),
            ("PERSON", "ORG"),
            ("ORG", "ORG"),
            ("PRODUCT", "PRODUCT"),
            ("PRODUCT", "ORG"),
        },
        "allows": {
            ("ORG", "ORG"),
            ("ORG", "PERSON"),
        },
        "supports": {
            ("ORG", "ORG"),
            ("ORG", "PRODUCT"),
            ("PERSON", "ORG"),
            ("PERSON", "PRODUCT"),
        },
        "retrieves": {
            ("ORG", "ORG"),
            ("ORG", "PRODUCT"),
            ("PERSON", "ORG"),
            ("PERSON", "PRODUCT"),
        },
        "matches": {
            ("ORG", "ORG"),
            ("ORG", "PRODUCT"),
            ("PRODUCT", "PRODUCT"),
        },
    }

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

        valid_entities = []

        for entity in entities:

            entity_text = entity.get(
                "text",
                "",
            ).strip()

            entity_label = entity.get(
                "label",
                "",
            ).strip()

            if not entity_text:
                continue

            if entity_label not in self.ALLOWED_ENTITY_LABELS:
                continue

            valid_entities.append(
                (
                    entity_text,
                    entity_label,
                )
            )

        if len(valid_entities) < 2:
            return []

        # -------------------------------------------------
        # Sentence-by-sentence extraction
        # -------------------------------------------------

        sentences = re.split(
            r"(?<=[.!?])\s+",
            normalized_text,
        )

        for sentence in sentences:

            sentence_lower = sentence.lower()

            sentence_entities = []

            # ---------------------------------------------
            # Find entity occurrences
            # ---------------------------------------------

            for entity_text, entity_label in valid_entities:

                start = 0

                while True:

                    position = sentence_lower.find(
                        entity_text.lower(),
                        start,
                    )

                    if position == -1:
                        break

                    sentence_entities.append(
                        (
                            position,
                            position + len(entity_text),
                            entity_text,
                            entity_label,
                        )
                    )

                    start = (
                        position
                        + len(entity_text)
                    )

            if len(sentence_entities) < 2:
                continue

            sentence_entities.sort(
                key=lambda item: item[0]
            )

            # ---------------------------------------------
            # Find relationship phrases
            # ---------------------------------------------

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

                        if (
                            not subject
                            or not object_entity
                        ):
                            continue

                        subject_position = (
                            self._find_entity_position(
                                sentence_entities,
                                subject,
                                relation_start,
                                before=True,
                            )
                        )

                        object_position = (
                            self._find_entity_position(
                                sentence_entities,
                                object_entity,
                                relation_end,
                                before=False,
                            )
                        )

                        if (
                            not subject_position
                            or not object_position
                        ):
                            continue

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

                        # ---------------------------------
                        # Type compatibility check
                        # ---------------------------------

                        subject_label = (
                            subject_position[3]
                        )

                        object_label = (
                            object_position[3]
                        )

                        if not self._valid_entity_types(
                            relationship_name,
                            subject_label,
                            object_label,
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

    # =====================================================
    # Find Subject
    # =====================================================

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

    # =====================================================
    # Find Object
    # =====================================================

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

    # =====================================================
    # Find Exact Entity Position
    # =====================================================

    @staticmethod
    def _find_entity_position(
        entities: list[tuple],
        entity_name: str,
        relation_position: int,
        before: bool,
    ):
        """
        Return the actual entity occurrence used by the
        relationship rather than relying only on its text.
        """

        candidates = []

        for entity in entities:

            start = entity[0]
            end = entity[1]
            text = entity[2]

            if text != entity_name:
                continue

            if before and end <= relation_position:
                candidates.append(entity)

            elif not before and start >= relation_position:
                candidates.append(entity)

        if not candidates:
            return None

        if before:
            return max(
                candidates,
                key=lambda item: item[1],
            )

        return min(
            candidates,
            key=lambda item: item[0],
        )

    # =====================================================
    # Entity Type Validation
    # =====================================================

    def _valid_entity_types(
        self,
        relationship_name: str,
        subject_label: str,
        object_label: str,
    ) -> bool:

        allowed_pairs = (
            self.RELATION_ENTITY_TYPES.get(
                relationship_name,
                set(),
            )
        )

        return (
            subject_label,
            object_label,
        ) in allowed_pairs


# =====================================================
# Singleton Service
# =====================================================

relationship_extraction_service = (
    RelationshipExtractionService()
)