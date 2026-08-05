from PIL import Image
import pytesseract

from app.core.ocr_config import (
    MIN_CONFIDENCE,
    TESSERACT_CONFIG,
)
from app.services.image_preprocessing_service import (
    image_preprocessing_service,
)


class OCRService:

    def extract_text(
        self,
        image: Image.Image,
    ) -> str:
        """
        Extract text from an image using OCR.
        """

        image = (
            image_preprocessing_service.preprocess(
                image
            )
        )

        return pytesseract.image_to_string(
            image,
            config=TESSERACT_CONFIG,
        ).strip()

    def extract_with_confidence(
        self,
        image: Image.Image,
    ):
        """
        Extract text and calculate average OCR confidence.
        """

        image = (
            image_preprocessing_service.preprocess(
                image
            )
        )

        data = pytesseract.image_to_data(
            image,
            config=TESSERACT_CONFIG,
            output_type=pytesseract.Output.DICT,
        )

        words = []
        confidences = []

        for text, confidence in zip(
            data["text"],
            data["conf"],
        ):
            text = text.strip()

            if not text:
                continue

            try:
                confidence = float(confidence)
            except ValueError:
                continue

            if confidence < MIN_CONFIDENCE:
                continue

            words.append(text)
            confidences.append(confidence)

        average_confidence = (
            sum(confidences) / len(confidences)
            if confidences
            else 0.0
        )

        return {
            "text": " ".join(words),
            "confidence": round(
                average_confidence,
                2,
            ),
        }


ocr_service = OCRService()