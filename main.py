from fastapi import FastAPI
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv
import os 

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
HASH = os.getenv('HASH')

app = FastAPI()

bcrypt_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")


from routes.films_routes import film_router
from routes.user_routes import user_router

app.include_router(film_router)
app.include_router(user_router)

