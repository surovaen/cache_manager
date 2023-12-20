from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse, JSONResponse

from app.core.helpers import upload_file
from app.database import get_database
from app.db.repository import avatar_repo
from app.models.avatar import AvatarBase


router = APIRouter()


@router.get(
    '/avatar',
    summary='Получение аватара автора',
    status_code=status.HTTP_200_OK,
)
async def get_avatar(
        author_id: str = None,
        avatar_id: str = None,
        conn: AsyncIOMotorClient = Depends(get_database),
):
    """Эндпоинт получения аватара автора."""
    if not (author_id or avatar_id):
        response = 'Не указан author_id и/или avatar_id'
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response,
        )

    avatar = await avatar_repo.filter(
        conn=conn,
        avatar_id=avatar_id,
        author_id=author_id,
    )
    if avatar:
        filepath = avatar[0].get('image')
        filename = Path(filepath).name

        return FileResponse(
            path=filepath,
            filename=filename,
            media_type='application/octet-stream',
        )

    response = 'Аватар не найден'
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=response,
    )


@router.post(
    '/avatar',
    summary='Загрузка аватара автора',
    status_code=status.HTTP_201_CREATED,
)
async def post_avatar(
        author_id: str,
        file: UploadFile = File(...),
        conn: AsyncIOMotorClient = Depends(get_database),
):
    """Эндпоинт загрузки аватара автора."""
    filepath = await upload_file(file)
    avatar = AvatarBase(
        image=filepath,
        author_id=author_id,
    )
    avatar_id = await avatar_repo.create(
        conn=conn,
        avatar=avatar,
    )

    return JSONResponse(
        content={'id': str(avatar_id)},
    )
