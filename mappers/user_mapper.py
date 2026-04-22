from fastapi.security import OAuth2PasswordRequestForm

from schemas.user_schemas import FavoriteFilmResponse, UserCreate, UserResponse
from schemas.token_schemas import TokenResponse
from models.models import FavoriteFilm, User


def from_request_create_user(user_create: UserCreate) -> dict:
    return {
        "name": user_create.name,
        "email": user_create.email,
        "password": user_create.password,
    }


def from_request_login(form_data: OAuth2PasswordRequestForm) -> dict:
    return {
        "email": form_data.username,
        "password": form_data.password,
    }


def from_request_refresh(refresh_token: str) -> dict:
    return {"refresh_token": refresh_token}


def to_response_token(access_token: str, refresh_token: str) -> TokenResponse:
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


def to_response_user(current_user: User, favorite_films: list[FavoriteFilm]) -> UserResponse:
    favorite_films_response = [
        FavoriteFilmResponse(
            film_id=film.film_id,
            film_name=film.film.name,
            user_id=film.user_id,
        )
        for film in favorite_films
    ]

    return UserResponse(
        name=current_user.name,
        email=current_user.email,
        favorite_films=favorite_films_response,
    )


def to_response_favorites_list(favorite_films: list[FavoriteFilm]) -> dict:
    return {
        "favorite_films": [
            {"id": film.film_id, "name": film.film.name} for film in favorite_films
        ]
    }
