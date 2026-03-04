from fastapi import APIRouter, Depends, HTTPException
from schemas.schemas import UserCreate, UserLogin, UserResponse, FilmResponse, FavoriteFilmResponse
from denpendencies.dependencies import get_session
from models.models import FavoriteFilm, User
from main import bcrypt_hash, SECRET_KEY, HASH
import jwt
from datetime import datetime, timedelta
user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/create") 
def create_user(user_create: UserCreate, session=Depends(get_session)):
    """Endpoint user create"""
    user  = session.query(User).filter(User.email==user_create.email).first()

    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    password_hash = bcrypt_hash.hash(user_create.password)
    new_user = User(name=user_create.name, email=user_create.email, password=password_hash) 
    session.add(new_user)
    session.commit()
    raise HTTPException(status_code=201, detail="User created successfully")

@user_router.post("/login")
def login_user(user_login: UserLogin, session=Depends(get_session)):
    user = session.query(User).filter(User.email == user_login.email).first()

    if not user or not bcrypt_hash.verify(user_login.password, user.password):
         
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Geração do token JWT
    payload = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(hours=1)  
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=HASH)
    
    return {"access_token": token, "token_type": "bearer"}


@user_router.get("/me")
def read_current_user(token: str, session=Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH])
        user_email = payload.get("sub")

        user = session.query(User).filter(User.email == user_email).first()

        favorite_films_response: list[FavoriteFilmResponse] = []
        favorite_films = session.query(FavoriteFilm).filter(FavoriteFilm.user_id == user.id).all()

        favorite_films_response = [
            FavoriteFilmResponse(
                film_name=film.film_name,
                user_id=film.user_id
            )
            for film in favorite_films
        ]
        return UserResponse(name=user.name, email=user.email, favorite_films=favorite_films_response)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@user_router.post("/add_favorite")
def add_favorite_film(token: str, film_name: str, session=Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH])
        user_gmail = payload.get("sub")

        user = session.query(User).filter(User.email == user_gmail).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        favorite_film = FavoriteFilm(film_name=film_name, user_id=user.id)
        session.add(favorite_film)
        session.commit()

        return {"message": "Film added to favorites"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

@user_router.patch("/remove_favorite")
def remove_favorite_film(token: str, film_name: str, session=Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH])
        user_gmail = payload.get("sub")

        user = session.query(User).filter(User.gmail == user_gmail).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        favorite_film = session.query(FavoriteFilm).filter(FavoriteFilm.film_name == film_name, FavoriteFilm.user_id == user.id).first()

        if not favorite_film:
            raise HTTPException(status_code=404, detail="Favorite film not found")

        session.delete(favorite_film)
        session.commit()

        return {"message": "Film removed from favorites"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

@user_router.patch("/update_password")
def update_password(token: str, new_password: str, session=Depends(get_session)):    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH])
        user_email = payload.get("sub")

        user = session.query(User).filter(User.email == user_email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_password_hash = bcrypt_hash.hash(new_password)
        user.password = new_password_hash
        session.commit()

        return {"message": "Password updated successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

@user_router.delete("/delete")
def delete_user(token: str, session=Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH])
        user_email = payload.get("sub")

        user = session.query(User).filter(User.email == user_email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        session.delete(user)
        session.commit()

        return {"message": "User deleted successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
user_router.get("/favorites")
def get_favorite_films(token: str, session=Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH])
        user_gmail = payload.get("sub")

        user = session.query(User).filter(User.gmail == user_gmail).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        favorite_films = session.query(FavoriteFilm).filter(FavoriteFilm.user_id == user.id).all()

        return {"favorite_films": [film.film_name for film in favorite_films]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    