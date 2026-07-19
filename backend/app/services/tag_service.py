class TagService:
    """Generates tags from extracted memory metadata."""

    def generate_tags(self, extraction) -> list[str]:
        tags = set()

        for person in extraction.people:
            tags.add(person.lower())

        for organization in extraction.organizations:
            tags.add(organization.lower())

        for location in extraction.locations:
            tags.add(location.lower())

        for date in extraction.dates:
            tags.add(date.lower())

        for event in extraction.events:
            tags.add(event.lower())

        for task in extraction.tasks:
            tags.add(task.lower())

        for goal in extraction.goals:
            tags.add(goal.lower())

        for preference in extraction.preferences:
            tags.add(preference.lower())

        return sorted(tags)


tag_service = TagService()