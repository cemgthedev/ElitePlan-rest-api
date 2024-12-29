# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

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

# Rota para pegar treino pelo id
@router.get("/workouts/{id}")
async def get_workout(id: int, db: Session = Depends(get_db)):
    try:
        workout = db.exec(select(Workout).where(Workout.id == id)).first()
        if workout is None:
            return {"error": "Workout not found"}
        return {"message": "Workout found successfully", "data": workout}
    except Exception as e:
        return {"error": str(e)}