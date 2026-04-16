# schemas.py
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    name: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class FilmRequest(BaseModel):
    name: str
    genre: str
    description: str
    release_year: int

    model_config = ConfigDict(from_attributes=True)


class FilmResponse(BaseModel):
    name: str
    genre: str
    description: str
    release_year: int

    model_config = ConfigDict(from_attributes=True)


class FavoriteFilmResponse(BaseModel):
    film_id: int
    film_name: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    name: str
    email: str
    favorite_films: list[FavoriteFilmResponse] = []

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
