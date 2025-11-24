from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token, decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession

# /auth/register,/auth/login , to keep main.py clean
router = APIRouter(prefix="/auth", tags=["auth"])
db_dependency= Annotated[AsyncSession,Depends(get_db)]

#reponse_model mean return only the fields I told you to, UserRead return only Id and email and not pwd
#payload is the JSON data sent by the client
#User is the ORM Model represents the user table, Python Class -> SQL Table
@router.post("/register", response_model=UserRead)
async def register(payload: UserCreate, db: db_dependency):

    existing = await db.execute(select(User).filter(User.email == payload.email))
    if existing.scalars().first():
        raise HTTPException(400, "Email already registered")

    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login")
async def login(payload: UserLogin, db: db_dependency):
    q = await db.execute(select(User).filter(User.email == payload.email))
    user = q.scalars().first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
