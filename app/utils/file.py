import os
import tempfile
from fastapi import UploadFile


async def save_upload_file_to_temp(upload_file: UploadFile) -> str:
    suffix = os.path.splitext(upload_file.filename or "")[1] or ".mp4"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        content = await upload_file.read()
        temp.write(content)
        return temp.name


def remove_file_safely(file_path: str) -> None:
    if file_path and os.path.exists(file_path):
        os.remove(file_path)