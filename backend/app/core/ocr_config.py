from pathlib import Path

import pytesseract


# ----------------------------------------------------
# Tesseract Installation
# ----------------------------------------------------

TESSERACT_PATH = Path(
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pytesseract.pytesseract.tesseract_cmd = str(
    TESSERACT_PATH
)

# ----------------------------------------------------
# OCR Configuration
# ----------------------------------------------------

# OCR Engine Mode
# 0 = Legacy
# 1 = Neural LSTM
# 2 = Legacy + LSTM
# 3 = Default

OCR_ENGINE_MODE = 3

# Page Segmentation Mode
# 3 = Fully automatic
# 6 = Single uniform block
# 11 = Sparse text

PAGE_SEGMENTATION_MODE = 6

# Ignore OCR below this confidence

MIN_CONFIDENCE = 50.0

# Final configuration passed to Tesseract

TESSERACT_CONFIG = (
    f"--oem {OCR_ENGINE_MODE} "
    f"--psm {PAGE_SEGMENTATION_MODE}"
)