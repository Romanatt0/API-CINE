# schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str

class FilmCreate(BaseModel):
    name: str
    genre: str
    description: str
    release_year: int
    

class FilmResponse(BaseModel):
    name: str
    genre: str
    description: str
    release_year: int

class FavoriteFilmResponse(BaseModel):
    film_name: str
    user_id: int

class UserResponse(BaseModel):
    name: str
    email: str
    favorite_films: list[FavoriteFilmResponse] = []