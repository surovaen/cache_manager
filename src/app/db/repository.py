from app.cache.author import AuthorCacheDecorator
from app.cache.avatar import AvatarCacheDecorator
from app.cache.book import BookCacheDecorator
from app.cache.manager.mapper import cache_manager
from app.db.author import AuthorRepository
from app.db.avatar import AvatarRepository
from app.db.book import BookRepository


author_repo = AuthorCacheDecorator(
    repository=AuthorRepository(),
    cache_manager=cache_manager(repo='author'),
)

book_repo = BookCacheDecorator(
    repository=BookRepository(),
    cache_manager=cache_manager(repo='book'),
    related_repository=author_repo,
)


avatar_repo = AvatarCacheDecorator(
    repository=AvatarRepository(),
    cache_manager=cache_manager(repo='avatar'),
)
