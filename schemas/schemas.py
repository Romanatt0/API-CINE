# schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str
    password: str

    class config:
        from_atributes = True


class UserLogin(BaseModel):
    email: str
    password: str
    class config:
        from_atributes = True

class FilmRequest(BaseModel):
    name: str
    genre: str
    description: str
    release_year: int

    class config:
        from_atributes = True

class FilmResponse(BaseModel):

    name: str
    genre: str
    description: str
    release_year: int

    class config:
        from_atributes = True

class FavoriteFilmResponse(BaseModel):
    film_name: str
    user_id: int

    class config:
        from_atributes = True

class UserResponse(BaseModel):
    name: str
    email: str
    favorite_films: list[FavoriteFilmResponse] = []

    class config:
        from_atributes = True