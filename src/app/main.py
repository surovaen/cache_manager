from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import settings
from app.api.urls import router as api_router
from app.database import close_mongodb_connection, connect_to_mongodb


title = 'Авторы и книги'
app = FastAPI(debug=settings.DEBUG, title=title)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler('startup', connect_to_mongodb)
app.add_event_handler('shutdown', close_mongodb_connection)

app.include_router(api_router, prefix='/api')
