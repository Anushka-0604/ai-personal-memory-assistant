from app.schemas.extraction import MemoryExtraction
from app.services.entity_extractor import EntityExtractor
from app.services.gemini_extractor import GeminiExtractor


class ExtractionService:
    """Coordinates all memory extraction components."""

    def __init__(self):
        self.entity_extractor = EntityExtractor()
        self.gemini_extractor = GeminiExtractor()

    def extract(self, text: str) -> MemoryExtraction:
        entity_result = self.entity_extractor.extract(text)
        gemini_result = self.gemini_extractor.extract(text)

        return self.merge(entity_result, gemini_result)

    def merge(
        self,
        entity_result: MemoryExtraction,
        gemini_result: MemoryExtraction,
    ) -> MemoryExtraction:

        return MemoryExtraction(
            people=list(
                set(entity_result.people + gemini_result.people)
            ),
            organizations=list(
                set(
                    entity_result.organizations
                    + gemini_result.organizations
                )
            ),
            locations=list(
                set(
                    entity_result.locations
                    + gemini_result.locations
                )
            ),
            dates=list(
                set(entity_result.dates + gemini_result.dates)
            ),
            events=list(
                set(entity_result.events + gemini_result.events)
            ),
            tasks=list(
                set(entity_result.tasks + gemini_result.tasks)
            ),
            goals=list(
                set(entity_result.goals + gemini_result.goals)
            ),
            preferences=list(
                set(
                    entity_result.preferences
                    + gemini_result.preferences
                )
            ),
            summary=(
                gemini_result.summary
                if gemini_result.summary
                else entity_result.summary
            ),
        )