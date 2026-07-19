class SentimentService:
    POSITIVE_WORDS = {
        "happy",
        "love",
        "like",
        "enjoy",
        "excellent",
        "good",
        "great",
        "success",
        "won",
        "favorite",
    }

    NEGATIVE_WORDS = {
        "sad",
        "hate",
        "bad",
        "angry",
        "failed",
        "problem",
        "issue",
        "pain",
        "sick",
        "stress",
    }

    def analyze(self, text: str):
        text = text.lower()

        positive = sum(
            word in text for word in self.POSITIVE_WORDS
        )

        negative = sum(
            word in text for word in self.NEGATIVE_WORDS
        )

        if positive > negative:
            return "Positive", 0.9

        if negative > positive:
            return "Negative", 0.9

        return "Neutral", 0.8


sentiment_service = SentimentService()