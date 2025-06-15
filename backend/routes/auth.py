from fastapi import FastAPI, Depends, HTTPException, APIRouter
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  Session
from utils.db import SessionLocal
from utils.auth import verify_password,create_access_token, get_current_user, get_user_by_email,

router =APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(SessionLocal)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    create_user(db, user)
    return {"msg": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(SessionLocal)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
