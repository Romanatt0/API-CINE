from sqlalchemy import String, create_engine, Column, Integer, ForeignKey,DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum
import datetime


db = create_engine("sqlite:///banco.db")
Base = declarative_base()

class Genre(str, Enum):
    ACTION = "Action"
    HORROR = "Horror"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    SCI_FI = "Sci-Fi"

class AccessLevel(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False,unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    access = Column(SqlEnum(AccessLevel), default=AccessLevel.USER)

    favorite_films = relationship("FavoriteFilm", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.access = AccessLevel.USER

class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True) 
    genre = Column(SqlEnum(Genre), nullable=False)
    release_year = Column(Integer, nullable=False)

    favorited_by = relationship("FavoriteFilm", back_populates="film", cascade="all, delete-orphan")

    def __init__(self, name, genre: Genre, release_year, description: str | None = None):
        self.name = name
        self.genre = genre
        self.release_year = release_year
        self.description = description

    
class FavoriteFilm(Base):
    __tablename__ = "favorite_films"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    film_id = Column(Integer, ForeignKey("films.id"), nullable=False)

    user = relationship("User", back_populates="favorite_films")
    film = relationship("Film", back_populates="favorited_by")

    def __init__(self, user_id, film_id):
        self.user_id = user_id
        self.film_id = film_id

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    film_id = Column(Integer, ForeignKey("films.id"), nullable=True)  # Null para replies
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)  # Self-reference
    comment_text = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

    # Relationships
    user = relationship("User")
    film = relationship("Film")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")

    def __init__(self, user_id, comment_text, film_id=None, parent_id=None):
        self.user_id = user_id
        self.film_id = film_id
        self.parent_id = parent_id
        self.comment_text = comment_text
        self.datetime = datetime.datetime.now()
