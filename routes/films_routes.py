from fastapi import APIRouter, Depends, HTTPException
from schemas.schemas import FilmRequest, FilmResponse
from denpendencies.dependencies import get_session
from models.models import Film, Genre

film_router = APIRouter(prefix="/films", tags=["films"])




@film_router.post("/create")
async def create_film(film_create: FilmRequest, session=Depends(get_session)):
    film = session.query(Film).filter(Film.name == film_create.name).first()

    if film:
        raise HTTPException(status_code=400, detail="Film already exists")
    
    if film_create.genre not in Genre.__members__:
        raise HTTPException(status_code=400, detail="Invalid genre")

    new_film = Film(name=film_create.name, description=film_create.description, genre=film_create.genre, release_year=film_create.release_year)
    session.add(new_film)
    session.commit()
    raise HTTPException(status_code=201, detail="Film created successfully")

@film_router.get("/{film_id}")
async def get_film(film_id: int, session=Depends(get_session)):
    film = session.query(Film).filter(Film.id == film_id).first()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    session.refresh(film)
    return FilmResponse(**film.__dict__)

@film_router.patch("/update/{film_id}")
async def update_film(film_id: int, film_update: FilmRequest, session=Depends(get_session)):
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
    raise HTTPException(status_code=200, detail="Film updated successfully")

@film_router.delete("/delete/{film_id}")
async def delete_film(film_id: int, session=Depends(get_session)):
    film = session.query(Film).filter(Film.id == film_id).first()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    session.delete(film)
    session.commit()
    raise HTTPException(status_code=200, detail="Film deleted successfully")


@film_router.get("/all")
async def get_all_films(session=Depends(get_session)):

    films: list[Film] = session.query(Film).all()  

    for film in films:
        session.refresh(film)
    return [FilmResponse(**film.__dict__) for film in films]