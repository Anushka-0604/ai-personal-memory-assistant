from pathlib import Path

from PIL import Image
from docx import Document
from pdf2image import convert_from_path
from pypdf import PdfReader
import pytesseract

from app.core import ocr_config


class DocumentExtractionService:

    def extract_text(
        self,
        file_path: str,
    ) -> str:

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self._extract_pdf(file_path)

        if extension == ".docx":
            return self._extract_docx(file_path)

        if extension == ".txt":
            return self._extract_txt(file_path)

        if extension in {
            ".jpg",
            ".jpeg",
            ".png",
        }:
            return self._extract_image(file_path)

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    def _extract_pdf(
        self,
        file_path: str,
    ) -> str:

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        text = text.strip()

        # ------------------------------------------------
        # OCR fallback for scanned PDFs
        # ------------------------------------------------
        if text:
            return text

        images = convert_from_path(file_path)

        ocr_text = ""

        for image in images:
            ocr_text += (
                pytesseract.image_to_string(image)
                + "\n"
            )

        return ocr_text.strip()

    def _extract_docx(
        self,
        file_path: str,
    ) -> str:

        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        ).strip()

    def _extract_txt(
        self,
        file_path: str,
    ) -> str:

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            return file.read().strip()

    def _extract_image(
        self,
        file_path: str,
    ) -> str:

        image = Image.open(file_path)

        return pytesseract.image_to_string(
            image
        ).strip()


document_extraction_service = (
    DocumentExtractionService()
)