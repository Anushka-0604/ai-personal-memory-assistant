import spacy

from app.schemas.extraction import MemoryExtraction


# Load the spaCy model once when the application starts
nlp = spacy.load("en_core_web_sm")


class EntityExtractor:
    """Extract named entities from text using spaCy."""

    def extract(self, text: str) -> MemoryExtraction:
        doc = nlp(text)

        extraction = MemoryExtraction()

        people = set()
        organizations = set()
        locations = set()
        dates = set()
        events = set()

        for entity in doc.ents:

            if entity.label_ == "PERSON":
                people.add(entity.text)

            elif entity.label_ == "ORG":
                organizations.add(entity.text)

            elif entity.label_ in ["GPE", "LOC"]:
                locations.add(entity.text)

            elif entity.label_ == "DATE":
                dates.add(entity.text)

            elif entity.label_ == "EVENT":
                events.add(entity.text)

        extraction.people = sorted(people)
        extraction.organizations = sorted(organizations)
        extraction.locations = sorted(locations)
        extraction.dates = sorted(dates)
        extraction.events = sorted(events)

        return extraction