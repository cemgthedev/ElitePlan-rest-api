# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime
from database import get_db
from models.plan import Plan
from models.workout import Workout
from models.plan_workouts import PlanWorkouts

# Criar roteador
router = APIRouter()

# Rota para adicionar um treino a um plano
@router.post("/plan_workouts")
async def create_plan_workout(plan_workout: PlanWorkouts, db: Session = Depends(get_db)):
    try:
        plan = db.exec(select(Plan).where(Plan.id == plan_workout.plan_id)).first()
        if plan is None:
            return {"error": "Plan not found"}
        
        workout = db.exec(select(Workout).where(Workout.id == plan_workout.workout_id)).first()
        if workout is None:
            return {"error": "Workout not found"}
        
        plan_workout.created_at = datetime.now()
        
        db.add(plan_workout)
        db.commit()
        db.refresh(plan_workout)
        return {"message": "Workout added to plan successfully", "data": plan_workout}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
# Rota para pegar treino para plano pelo id
@router.get("/plan_workouts/{id}")
async def get_plan_workout(id: int, db: Session = Depends(get_db)):
    try:
        plan_workout = db.exec(select(PlanWorkouts).where(PlanWorkouts.id == id)).first()
        if plan_workout is None:
            return {"error": "Plan workout not found"}
        return {"message": "Plan workout found successfully", "data": plan_workout}
    except Exception as e:
        return {"error": str(e)}