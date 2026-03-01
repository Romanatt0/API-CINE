from fastapi import APIRouter, Depends, HTTPException
from schemas import FilmCreate, FilmResponse
from dependencies import get_session
from models import Film, Genre

film_router = APIRouter(prefix="/films", tags=["films"])




@film_router.post("/create")
def create_film(film_create: FilmCreate, session=Depends(get_session)):
    film = session.query(Film).filter(Film.name == film_create.name).first()

    if film:
        raise HTTPException(status_code=400, detail="Film already exists")
    
    if film_create.genre not in Genre.__members__:
        raise HTTPException(status_code=400, detail="Invalid genre")

    new_film = Film(name=film_create.name, description=film_create.description, genre=film_create.genre, release_year=film_create.release_year)
    session.add(new_film)
    session.commit()
    raise HTTPException(status_code=201, detail="Film created successfully")


@film_router.get("/all")
def get_all_films(session=Depends(get_session)):

    films: list[Film] = session.query(Film).all()  

    for film in films:
        session.refresh(film)
    return [FilmResponse(**film.__dict__) for film in films]