from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from passlib.hash import pbkdf2_sha256
from sqlmodel import select

from app.database import Session, create_db_and_tables, get_session
from app.models import User, UserCreate, UserPublic


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/users", response_model=UserPublic)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    hashed_password = pbkdf2_sha256.hash(user.password.get_secret_value())
    db_user = User.model_validate(user, update={"password_hash": hashed_password})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users", response_model=list[UserPublic])
async def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@app.get("/users/{user_id}", response_model=UserPublic)
async def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
