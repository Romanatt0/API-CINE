from fastapi import APIRouter, Depends, HTTPException
from schemas import FilmCreate
from dependencies import get_session
from models import Film

film_router = APIRouter(prefix="/films", tags=["films"])


film_router.get()
def find_all_films(films: list[FilmCreate], session=Depends(get_session)):

    films: list[Film] = session.query(Film)