from fastapi import APIRouter

from app.api.v1.author import router as author_router
from app.api.v1.avatar import router as avatar_router
from app.api.v1.book import router as book_router


router = APIRouter()

router.include_router(author_router, tags=['authors'])
router.include_router(book_router, tags=['books'])
router.include_router(avatar_router, tags=['avatars'])
