from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.schemas import UserCreate, UserResponse, FavoriteFilmResponse, TokenResponse
from dependencies.dependencies import get_session
from models.models import FavoriteFilm, User
from auth.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from auth.dependencies import get_current_user
import jwt

user_router = APIRouter(prefix="/users", tags=["users"])


# ──────────────────────────────────────────────
# Registro
# ──────────────────────────────────────────────
@user_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """Cria um novo usuário."""
    user = session.query(User).filter(User.email == user_create.email).first()

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    password_hashed = hash_password(user_create.password)
    new_user = User(name=user_create.name, email=user_create.email, password=password_hashed)
    session.add(new_user)
    session.commit()

    return {"message": "User created successfully"}


# ──────────────────────────────────────────────
# Login — endpoint OAuth2 padrão
# ──────────────────────────────────────────────
@user_router.post("/login", response_model=TokenResponse)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """
    Endpoint de login OAuth2.
    Recebe form data com campos 'username' (email) e 'password'.
    Retorna access_token + refresh_token.
    """
    user = session.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


# ──────────────────────────────────────────────
# Refresh token
# ──────────────────────────────────────────────
@user_router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, session: Session = Depends(get_session)):
    """
    Recebe um refresh token válido e retorna um novo par de tokens.
    """
    try:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido. Envie um refresh token.",
            )

        user_email = payload.get("sub")
        user = session.query(User).filter(User.email == user_email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_access_token = create_access_token(data={"sub": user.email})
        new_refresh_token = create_refresh_token(data={"sub": user.email})

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Refresh token inválido")


# ──────────────────────────────────────────────
# Endpoints protegidos — usam Depends(get_current_user)
# ──────────────────────────────────────────────
@user_router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Retorna dados do usuário autenticado e seus filmes favoritos."""
    favorite_films = (
        session.query(FavoriteFilm)
        .filter(FavoriteFilm.user_id == current_user.id)
        .all()
    )

    favorite_films_response = [
        FavoriteFilmResponse(film_name=film.film_name, user_id=film.user_id)
        for film in favorite_films
    ]

    return UserResponse(
        name=current_user.name,
        email=current_user.email,
        favorite_films=favorite_films_response,
    )


@user_router.post("/add_favorite")
async def add_favorite_film(
    film_name: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Adiciona um filme aos favoritos do usuário autenticado."""
    favorite_film = FavoriteFilm(film_name=film_name, user_id=current_user.id)
    session.add(favorite_film)
    session.commit()

    return {"message": "Film added to favorites"}


@user_router.patch("/remove_favorite")
async def remove_favorite_film(
    film_name: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Remove um filme dos favoritos do usuário autenticado."""
    favorite_film = (
        session.query(FavoriteFilm)
        .filter(
            FavoriteFilm.film_name == film_name,
            FavoriteFilm.user_id == current_user.id,
        )
        .first()
    )

    if not favorite_film:
        raise HTTPException(status_code=404, detail="Favorite film not found")

    session.delete(favorite_film)
    session.commit()

    return {"message": "Film removed from favorites"}


@user_router.patch("/update_password")
async def update_password(
    new_password: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Atualiza a senha do usuário autenticado."""
    current_user.password = hash_password(new_password)
    session.commit()

    return {"message": "Password updated successfully"}


@user_router.delete("/delete")
async def delete_user(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Deleta a conta do usuário autenticado."""
    session.delete(current_user)
    session.commit()

    return {"message": "User deleted successfully"}


@user_router.get("/favorites")
async def get_favorite_films(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Lista os filmes favoritos do usuário autenticado."""
    favorite_films = (
        session.query(FavoriteFilm)
        .filter(FavoriteFilm.user_id == current_user.id)
        .all()
    )

    return {"favorite_films": [film.film_name for film in favorite_films]}
