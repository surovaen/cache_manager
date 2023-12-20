from pathlib import Path
from typing import List
import uuid

import aiofiles
from fastapi import UploadFile

from app import settings


async def upload_file(file: UploadFile) -> str:
    """Сохранение файла."""
    ext = Path(file.filename).suffix
    filename = uuid.uuid4()
    filepath = '{media}/{file}{ext}'.format(
        media=settings.MEDIA_DIR,
        file=filename,
        ext=ext,
    )

    async with aiofiles.open(filepath, 'wb') as saved_file:
        while content := await file.read(1024):
            await saved_file.write(content)

    return filepath


def process_object_id(value: List[dict]) -> List[dict]:
    """Перевод ObjectId в строку."""
    result = []

    for item in value:
        object_id = item.pop('_id')
        item['_id'] = str(object_id)
        result.append(item)

    return result
