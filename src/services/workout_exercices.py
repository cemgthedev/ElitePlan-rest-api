from math import ceil
from fastapi import APIRouter, Depends, Query
from sqlalchemy.sql import func
from sqlmodel import Session, select
from datetime import datetime
from database import get_db
from models.workout import Workout
from models.exercice import Exercice
from models.workout_exercices import WorkoutExercices
from services.configs import workout_exercices_logger as logger

# Criar roteador
router = APIRouter()

# Rota para adicionar um exercício a um treino
@router.post("/workout_exercices")
async def create_workout_exercice(workout_exercice: WorkoutExercices, db: Session = Depends(get_db)):
    try:
        logger.info(f"Adicionando exercicio {workout_exercice.exercice_id} ao treino {workout_exercice.workout_id}")
        workout = db.exec(select(Workout).where(Workout.id == workout_exercice.workout_id)).first()
        if workout is None:
            logger.warning(f"Treino com ID {workout_exercice.workout_id} nao encontrado")
            return {"error": "Workout not found"}
        
        exercice = db.exec(select(Exercice).where(Exercice.id == workout_exercice.exercice_id)).first()
        if exercice is None:
            logger.warning(f"Exercício com ID {workout_exercice.exercice_id} nao encontrado")
            return {"error": "Exercice not found"}
        
        workout_exercice.created_at = datetime.now()
        
        db.add(workout_exercice)
        db.commit()
        db.refresh(workout_exercice)
        
        logger.info(f"Exercício adicionado ao treino com sucesso!")
        return {"message": "Exercice added to workout successfully", "data": workout_exercice}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao adicionar um exercício ao treino: {str(e)}")
        return {"error": str(e)}
    
# Rota para remover um exercício de um treino
@router.delete("/workout_exercices/{id}")
async def delete_workout_exercice(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Removendo exercício {id} do treino")
        workout_exercice = db.exec(select(WorkoutExercices).where(WorkoutExercices.id == id)).first()
        if workout_exercice is None:
            logger.warning(f"Exercício com ID {id} nao encontrado")
            return {"error": "Workout exercice not found"}
        
        db.delete(workout_exercice)
        db.commit()
        
        logger.info(f"Exercício removido do treino com sucesso!")
        return {"message": "Workout exercice deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover um exercício do treino: {str(e)}")
        return {"error": str(e)}
    
# Rota para pegar exercício para treino pelo id
@router.get("/workout_exercices/{id}")
async def get_workout_exercice(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Buscando exercício {id} do treino")
        workout_exercice = db.exec(select(WorkoutExercices).where(WorkoutExercices.id == id)).first()
        if workout_exercice is None:
            logger.warning(f"Exercício com ID {id} nao encontrado")
            return {"error": "Workout exercice not found"}
        
        logger.info(f"Exercício encontrado: {workout_exercice}")
        return {"message": "Workout exercice found successfully", "data": workout_exercice}
    except Exception as e:
        logger.error(f"Erro ao buscar um exercício: {str(e)}")
        return {"error": str(e)}
    
# Rota para listar exercícios para treino
@router.get("/workout_exercices")
async def get_workout_exercices(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page (max 100)")
):
    try:
        logger.info(f"Buscando exercicios...")
        offset = (page - 1) * limit
        stmt = select(WorkoutExercices).offset(offset).limit(limit)
        workout_exercices = db.exec(stmt).all()

        total_workout_exercices = db.exec(select(func.count()).select_from(WorkoutExercices)).first()
        total_pages = ceil(total_workout_exercices / limit)
        
        if total_workout_exercices > 0:
            logger.info(f"Exercicios encontrados: {total_workout_exercices}")
        else:
            logger.warning(f"Exercicios nao encontrados")

        return {
            "message": "Workout exercices found successfully",
            "data": workout_exercices,
            "page": page,
            "limit": limit,
            "total_workout_exercices": total_workout_exercices,
            "total_pages": total_pages
        }
    except Exception as e:
        logger.error(f"Erro ao buscar exercicios: {str(e)}")
        return {"error": str(e)}
    
# Rota para retorno da quantidade de exercícios para treinos
@router.get("/quantity/workout_exercices")
async def get_workout_exercices_quantity(db: Session = Depends(get_db)):
    try:
        logger.info(f"Calculando quantidade de exercícios para treinos...")
        quantity = db.exec(select(func.count()).select_from(WorkoutExercices)).first()
        
        logger.info(f"Quantidade de exercícios para treinos encontrados: {quantity}")
        return {"message": "Workout exercices quantity found successfully", "data": str(quantity)}
    except Exception as e:
        logger.error(f"Erro ao calcular a quantidade de exercícios para treinos: {str(e)}")
        return {"error": str(e)}