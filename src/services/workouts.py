# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_db
from models.workout import Workout

# Criar roteador
router = APIRouter()

# Rota para criar um novo exercício
@router.post("/workouts")
async def create_user(workout: Workout, db: Session = Depends(get_db)):
    try:
        db.add(workout)
        db.commit()
        return {"message": "Workout created successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}