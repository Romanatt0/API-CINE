from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.schemas import FilmRequest, FilmResponse
from dependencies.dependencies import get_session
from models.models import Film, Genre, User
from auth.dependencies import get_current_user

film_router = APIRouter(prefix="/films", tags=["films"])


# ──────────────────────────────────────────────
# Endpoints públicos (leitura)
# ──────────────────────────────────────────────
@film_router.get("/all", response_model=list[FilmResponse])
async def get_all_films(session: Session = Depends(get_session)):
    """Lista todos os filmes. Endpoint público."""
    films: list[Film] = session.query(Film).all()

    for film in films:
        session.refresh(film)

    return [FilmResponse(**film.__dict__) for film in films]


@film_router.get("/{film_id}", response_model=FilmResponse)
async def get_film(film_id: int, session: Session = Depends(get_session)):
    """Busca um filme por ID. Endpoint público."""
    film = session.query(Film).filter(Film.id == film_id).first()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    session.refresh(film)
    return FilmResponse(**film.__dict__)


# ──────────────────────────────────────────────
# Endpoints protegidos (escrita) — requerem autenticação
# ──────────────────────────────────────────────
@film_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=dict)
async def create_film(
    film_create: FilmRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Cria um novo filme. Requer autenticação."""
    film = session.query(Film).filter(Film.name == film_create.name).first()

    if film:
        raise HTTPException(status_code=400, detail="Film already exists")

    if film_create.genre not in Genre.__members__:
        raise HTTPException(status_code=400, detail="Invalid genre")

    new_film = Film(
        name=film_create.name,
        description=film_create.description,
        genre=film_create.genre,
        release_year=film_create.release_year,
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
    film = session.query(Film).filter(Film.id == film_id).first()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    if film_update.genre not in Genre.__members__:
        raise HTTPException(status_code=400, detail="Invalid genre")

    film.name = film_update.name
    film.description = film_update.description
    film.genre = film_update.genre
    film.release_year = film_update.release_year

    session.commit()

    return {"message": "Film updated successfully"}


@film_router.delete("/delete/{film_id}")
async def delete_film(
    film_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Deleta um filme. Requer autenticação."""
    film = session.query(Film).filter(Film.id == film_id).first()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    session.delete(film)
    session.commit()

    return {"message": "Film deleted successfully"}
