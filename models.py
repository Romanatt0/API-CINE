from sqlalchemy import String, create_engine, Column, Integer, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum


db = create_engine("sqlite:///banco.db")
Base = declarative_base()

class Genre(str, Enum):
    ACTION = "Action"
    HORROR = "Horror"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    SCI_FI = "Sci-Fi"



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False,unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    favorite_films = relationship("FavoriteFilm", back_populates="user", cascade="all, delete-orphan")

    def __ini__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True) 
    genre = Column(SqlEnum(Genre), nullable=False)
    release_year = Column(Integer, nullable=False)

    def __init__(self, name, genre: Genre, release_year, description: str | None = None):
        self.name = name
        self.genre = genre
        self.release_year = release_year
        self.description = description

    

class FavoriteFilm(Base):
    __tablename__ = "favorite_films"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    film_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="favorite_films")

    def __init__(self, film_name, user_id):
        self.film_name = film_name
        self.user_id = user_id
