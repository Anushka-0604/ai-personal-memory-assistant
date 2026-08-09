import spacy


class NERService:
    """
    Extracts named entities from document text using spaCy.
    """

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text: str) -> list[dict]:
        """
        Extract named entities from the given text.
        """

        if not text or not text.strip():
            return []

        doc = self.nlp(text)

        entities = []

        for entity in doc.ents:
            entities.append(
                {
                    "text": entity.text,
                    "label": entity.label_,
                    "description": spacy.explain(entity.label_),
                }
            )

        return entities


ner_service = NERService()