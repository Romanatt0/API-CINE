from src.schemas.film_schemas import FilmRequest, FilmResponse
from src.models.models import Film


def from_request_film(film_request: FilmRequest) -> dict:
    return {
        "name": film_request.name,
        "description": film_request.description,
        "genre": film_request.genre,
        "release_year": film_request.release_year,
    }


def to_response_film(film: Film) -> FilmResponse:
    return FilmResponse(
        name=film.name,
        genre=film.genre,
        description=film.description,
        release_year=film.release_year,
    )


def to_response_film_list(films: list[Film]) -> list[FilmResponse]:
    return [to_response_film(film) for film in films]
