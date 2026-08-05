from pathlib import Path

import pytesseract


TESSERACT_PATH = (
    Path(
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
)

pytesseract.pytesseract.tesseract_cmd = str(
    TESSERACT_PATH
)