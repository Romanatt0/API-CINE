from fastapi import FastAPI
from cinema_routes import router

app = FastAPI()

app.include_router(router)