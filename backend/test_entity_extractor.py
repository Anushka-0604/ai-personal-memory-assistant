from app.services.entity_extractor import EntityExtractor

extractor = EntityExtractor()

result = extractor.extract(
    """
    John met Alice at Microsoft in Bangalore yesterday.
    John will attend the Olympics next year.
    """
)

print(result)