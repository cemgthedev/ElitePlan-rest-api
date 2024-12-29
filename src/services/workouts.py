# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy.sql import func
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
    
# Rota para listar treinos
@router.get("/workouts")
async def get_workouts(db: Session = Depends(get_db)):
    try:
        workouts = db.exec(select(Workout)).all()
        return {"message": "Workouts found successfully", "data": workouts}
    except Exception as e:
        return {"error": str(e)}
    
# Rota para retorno da quantidade de treinos
@router.get("/quantity/workouts")
async def get_workouts_quantity(db: Session = Depends(get_db)):
    try:
        quantity = db.exec(select(func.count()).select_from(Workout)).first()
        return {"message": "Workouts quantity found successfully", "data": str(quantity)}
    except Exception as e:
        return {"error": str(e)}