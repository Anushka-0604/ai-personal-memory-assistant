from datetime import datetime, timedelta


class TemporalService:
    """Extracts and reasons about simple temporal expressions."""

    def extract_date(self, text: str):
        text = text.lower()

        today = datetime.now().date()

        if "today" in text:
            return today

        if "tomorrow" in text:
            return today + timedelta(days=1)

        if "yesterday" in text:
            return today - timedelta(days=1)

        return None


temporal_service = TemporalService()