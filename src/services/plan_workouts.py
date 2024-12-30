from math import ceil
from fastapi import APIRouter, Depends, Query
from sqlalchemy.sql import func
from sqlmodel import Session, select
from datetime import datetime
from database import get_db
from models.plan import Plan
from models.workout import Workout
from models.plan_workouts import PlanWorkouts
from services.configs import plan_workouts_logger as logger

# Criar roteador
router = APIRouter()

# Rota para adicionar um treino a um plano
@router.post("/plan_workouts")
async def create_plan_workout(plan_workout: PlanWorkouts, db: Session = Depends(get_db)):
    try:
        logger.info(f"Adicionando um treino ao plano...")
        plan = db.exec(select(Plan).where(Plan.id == plan_workout.plan_id)).first()
        if plan is None:
            logger.warning(f"Plano com ID {plan_workout.plan_id} nao encontrado")
            return {"error": "Plan not found"}
        
        workout = db.exec(select(Workout).where(Workout.id == plan_workout.workout_id)).first()
        if workout is None:
            logger.warning(f"Treino com ID {plan_workout.workout_id} nao encontrado")
            return {"error": "Workout not found"}
        
        plan_workout.created_at = datetime.now()
        
        db.add(plan_workout)
        db.commit()
        db.refresh(plan_workout)
        
        logger.info(f"Treino adicionado ao plano com sucesso!")
        return {"message": "Workout added to plan successfully", "data": plan_workout}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao adicionar um treino ao plano: {str(e)}")
        return {"error": str(e)}

# Rota para deletar um treino de um plano pelo id
@router.delete("/plan_workouts/{id}")
async def delete_plan_workout(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Removendo um treino de um plano...")
        plan_workout = db.exec(select(PlanWorkouts).where(PlanWorkouts.id == id)).first()
        if plan_workout is None:
            logger.warning(f"Treino de um plano com ID {id} nao encontrado")
            return {"error": "Plan workout not found"}
        
        db.delete(plan_workout)
        db.commit()
        
        logger.info(f"Treino de um plano removido com sucesso!")
        return {"message": "Plan workout deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover um treino de um plano: {str(e)}")
        return {"error": str(e)}
    
# Rota para pegar treino para plano pelo id
@router.get("/plan_workouts/{id}")
async def get_plan_workout(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Buscando um treino de um plano pelo ID...")
        plan_workout = db.exec(select(PlanWorkouts).where(PlanWorkouts.id == id)).first()
        if plan_workout is None:
            logger.warning(f"Treino de um plano com ID {id} nao encontrado")
            return {"error": "Plan workout not found"}
        
        logger.info(f"Treino de um plano encontrado: {plan_workout}")
        return {"message": "Plan workout found successfully", "data": plan_workout}
    except Exception as e:
        logger.error(f"Erro ao buscar um treino de um plano: {str(e)}")
        return {"error": str(e)}
    
# Rota para listar treinos para planos
@router.get("/plan_workouts")
async def get_plan_workouts(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page (max 100)")
):
    try:
        logger.info(f"Buscando treinos para planos...")
        offset = (page - 1) * limit
        stmt = select(PlanWorkouts).offset(offset).limit(limit)
        plan_workouts = db.exec(stmt).all()

        total_plan_workouts = db.exec(select(func.count()).select_from(PlanWorkouts)).first()
        total_pages = ceil(total_plan_workouts / limit)
        
        if total_plan_workouts > 0:
            logger.info(f"Treinos para planos encontrados!")
        else:
            logger.warning(f"Treinos para planos nao encontrados")

        return {
            "message": "Plan workouts found successfully",
            "data": plan_workouts,
            "page": page,
            "limit": limit,
            "total_plan_workouts": total_plan_workouts,
            "total_pages": total_pages
        }
    except Exception as e:
        logger.error(f"Erro ao buscar treinos para planos: {str(e)}")
        return {"error": str(e)}
    
# Rota para retorno da quantidade de treinos para planos
@router.get("/quantity/plan_workouts")
async def get_plan_workouts_quantity(db: Session = Depends(get_db)):
    try:
        logger.info(f"Calculando quantidade de treinos para planos...")
        quantity = db.exec(select(func.count()).select_from(PlanWorkouts)).first()
        
        logger.info(f"Quantidade de treinos para planos encontrados: {quantity}")
        return {"message": "Plan workouts quantity found successfully", "data": str(quantity)}
    except Exception as e:
        logger.error(f"Erro ao calcular a quantidade de treinos para planos: {str(e)}")
        return {"error": str(e)}