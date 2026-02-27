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
    
