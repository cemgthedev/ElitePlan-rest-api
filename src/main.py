from fastapi import FastAPI, Depends
from sqlmodel import Session
from database import get_db
from models import *
from services.users import router as users_router

app = FastAPI()

@app.get("/")
def get_db(db: Session = Depends(get_db)):
    if db is None:
        return {"message": "Database not connected"}
    return {"message": "Database connected"}

app.include_router(users_router)