from app.services.gemini_extractor import GeminiExtractor

extractor = GeminiExtractor()

result = extractor.extract(
    """
    I want to get an internship at Google next summer.
    I prefer remote work.
    Remind me to update my resume tomorrow.
    """
)

print(result)
