from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status


UPLOAD_DIRECTORY = Path("uploads/documents")

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def save_file(
    file: UploadFile,
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file selected.",
        )

    extension = Path(file.filename).suffix.lower()
    print(f"Detected extension: {extension}") 
    
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported file type. "
                "Only PDF, DOCX, and TXT files are allowed."
            ),
        )

    file_bytes = file.file.read()

    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 10 MB limit.",
        )

    filename = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIRECTORY / filename

    with open(file_path, "wb") as buffer:
        buffer.write(file_bytes)

    return {
        "filename": filename,
        "original_filename": file.filename,
        "file_type": extension,
        "file_size": len(file_bytes),
        "file_path": str(file_path),
    }