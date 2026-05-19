from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas.film_schemas import FilmRequest, FilmResponse
from src.dependencies.dependencies import get_session
from src.models.models import Film, Genre, User
from src.auth.dependencies import get_current_user
from src.mappers.film_mapper import from_request_film, to_response_film, to_response_film_list

film_router = APIRouter(prefix="/films", tags=["films"])


@film_router.get("/all", response_model=list[FilmResponse])
async def get_all_films(session: Session = Depends(get_session)):
    """Lista todos os filmes. Endpoint público."""
    films: list[Film] = session.query(Film).all()

    for film in films:
        session.refresh(film)

    return to_response_film_list(films)


@film_router.get("/{film_id}", response_model=FilmResponse)
async def get_film(film_id: int, session: Session = Depends(get_session)):
    """Busca um filme por ID. Endpoint público."""
    film = session.query(Film).filter(Film.id == film_id).first()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    session.refresh(film)
    return to_response_film(film)


@film_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=dict)
async def create_film(
    film_create: FilmRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Cria um novo filme. Requer autenticação."""

    if current_user.access != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    payload = from_request_film(film_create)
    film = session.query(Film).filter(Film.name == payload["name"]).first()

    if film:
        raise HTTPException(status_code=400, detail="Film already exists")

    if payload["genre"] not in Genre.__members__:
        raise HTTPException(status_code=400, detail="Invalid genre")

    new_film = Film(
        name=payload["name"],
        description=payload["description"],
        genre=payload["genre"],
        release_year=payload["release_year"],
    )
    session.add(new_film)
    session.commit()

    return {"message": "Film created successfully"}


@film_router.patch("/update/{film_id}")
async def update_film(
    film_id: int,
    film_update: FilmRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Atualiza um filme existente. Requer autenticação."""

    if current_user.access != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    film = session.query(Film).filter(Film.id == film_id).first()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    payload = from_request_film(film_update)
    if payload["genre"] not in Genre.__members__:
        raise HTTPException(status_code=400, detail="Invalid genre")

    film.name = payload["name"]
    film.description = payload["description"]
    film.genre = payload["genre"]
    film.release_year = payload["release_year"]

    session.commit()

    return {"message": "Film updated successfully"}


@film_router.delete("/delete/{film_id}")
async def delete_film(
    film_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Deleta um filme. Requer autenticação."""

    if current_user.access != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    film = session.query(Film).filter(Film.id == film_id).first()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    session.delete(film)
    session.commit()

    return {"message": "Film deleted successfully"}
