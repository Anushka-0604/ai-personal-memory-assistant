from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIRECTORY = Path("uploads/documents")


UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


def save_file(
    file: UploadFile,
):
    extension = Path(file.filename).suffix

    filename = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIRECTORY / filename

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "filename": filename,
        "original_filename": file.filename,
        "file_type": extension.lower(),
        "file_size": file_path.stat().st_size,
        "file_path": str(file_path),
    }