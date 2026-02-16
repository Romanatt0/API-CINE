from fastapi import FastAPI
from passlib.context import CryptContext

app = FastAPI()

bcrypt_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")


from cinema_routes import router
from user_routes import user_router

app.include_router(router)
app.include_router(user_router)

