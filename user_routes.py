from fastapi import APIRouter, Depends, HTTPException
from schemas import UserCreate
from dependencies import get_session
from models import User
from main import bcrypt_hash

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/create") 
def create_user(user_create: UserCreate, session=Depends(get_session)):
    user  = session.query(User).filter(User.email==user_create.email).first()

    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    password_hash = bcrypt_hash.hash(user_create.password)
    new_user = User(name=user_create.name, email=user_create.email, password=password_hash) 
    session.add(new_user)
    session.commit()
    raise HTTPException(status_code=201, detail="User created successfully")

@user_router.post("/login")
def login_user(user_create: UserCreate, session=Depends(get_session)):
    user = session.query(User).filter(User.email==user_create.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not bcrypt_hash.verify(user_create.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    raise HTTPException(status_code=200, detail="Login successful")

    
    