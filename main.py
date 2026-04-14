from fastapi import FastAPI

app = FastAPI(
    title="Cinema Social Network API",
    description="API de rede social de cinema com autenticação OAuth2",
    version="1.0.0",
)

from routes.films_routes import film_router
from routes.user_routes import user_router

app.include_router(film_router)
app.include_router(user_router)
