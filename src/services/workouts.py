# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_db
from models.workout import Workout

# Criar roteador
router = APIRouter()

# Rota para criar um novo exercício
@router.post("/workouts")
async def create_workout(workout: Workout, db: Session = Depends(get_db)):
    try:
        db.add(workout)
        db.commit()
        db.refresh(workout)
        return {"message": "Workout created successfully", "data": workout}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}