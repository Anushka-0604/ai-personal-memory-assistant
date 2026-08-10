import re

import spacy


class NERService:
    """
    Extracts meaningful named entities from document text using spaCy.
    """

    # Entity types that are useful for our knowledge graph.
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

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text: str) -> list[dict]:
        """
        Extract meaningful named entities from the given text.
        """

        if not text or not text.strip():
            return []

        doc = self.nlp(text)

        entities = []
        seen = set()

        for entity in doc.ents:

            entity_text = entity.text.strip()
            label = entity.label_

            # Ignore unsupported entity types.
            if label not in self.ALLOWED_LABELS:
                continue

            # Ignore empty entities.
            if not entity_text:
                continue

            # Ignore entities that are only numbers/symbols.
            if not re.search(r"[A-Za-z]", entity_text):
                continue

            # Clean excessive whitespace/newlines caused by PDFs.
            entity_text = re.sub(
                r"\s+",
                " ",
                entity_text,
            ).strip()

            # Ignore very short noisy entities.
            if len(entity_text) < 2:
                continue

            # Ignore entities that are mostly symbols.
            if not re.search(
                r"[A-Za-z]{2,}",
                entity_text,
            ):
                continue

            # Avoid duplicate entities.
            key = (
                entity_text.lower(),
                label,
            )

            if key in seen:
                continue

            seen.add(key)

            entities.append(
                {
                    "text": entity_text,
                    "label": label,
                    "description": spacy.explain(label),
                }
            )

        return entities


ner_service = NERService()