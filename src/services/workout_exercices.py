# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime
from database import get_db
from models.workout import Workout
from models.exercice import Exercice
from models.workout_exercices import WorkoutExercices

# Criar roteador
router = APIRouter()

# Rota para adicionar um exercício a um treino
@router.post("/workout_exercices")
async def create_workout_exercice(workout_exercice: WorkoutExercices, db: Session = Depends(get_db)):
    try:
        workout = db.exec(select(Workout).where(Workout.id == workout_exercice.workout_id)).first()
        if workout is None:
            return {"error": "Workout not found"}
        
        exercice = db.exec(select(Exercice).where(Exercice.id == workout_exercice.exercice_id)).first()
        if exercice is None:
            return {"error": "Exercice not found"}
        
        workout_exercice.created_at = datetime.now()
        
        db.add(workout_exercice)
        db.commit()
        db.refresh(workout_exercice)
        return {"message": "Exercice added to workout successfully", "data": workout_exercice}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
# Rota para pegar exercício para treino pelo id
@router.get("/workout_exercices/{id}")
async def get_workout_exercice(id: int, db: Session = Depends(get_db)):
    try:
        workout_exercice = db.exec(select(WorkoutExercices).where(WorkoutExercices.id == id)).first()
        if workout_exercice is None:
            return {"error": "Workout exercice not found"}
        return {"message": "Workout exercice found successfully", "data": workout_exercice}
    except Exception as e:
        return {"error": str(e)}