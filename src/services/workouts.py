# Criar roteador
from math import ceil
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, and_, select
from sqlalchemy.sql import func
from database import get_db
from models.workout import Workout
from services.configs import workouts_logger as logger

# Criar roteador
router = APIRouter()

# Rota para criar um novo treino
@router.post("/workouts")
async def create_workout(workout: Workout, db: Session = Depends(get_db)):
    try:
        logger.info(f"Criando um novo treino...")
        db.add(workout)
        db.commit()
        db.refresh(workout)
        
        logger.info(f"Treino criado com sucesso!")
        return {"message": "Workout created successfully", "data": workout}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar um novo treino: {str(e)}")
        return {"error": str(e)}
    
# Rota para atualizar um treino
@router.put("/workouts/{id}")
async def update_workout(id: int, updated_workout: Workout, db: Session = Depends(get_db)):
    try:
        logger.info(f"Atualizando treino com ID: {id}")
        workout = db.exec(select(Workout).where(Workout.id == id)).first()
        if workout is None:
            logger.warning(f"Treino com ID {id} nao encontrado")
            return {"error": "Workout not found"}
        workout.title = updated_workout.title
        workout.description = updated_workout.description
        workout.rest_time = updated_workout.rest_time
        workout.type = updated_workout.type
        workout.category = updated_workout.category
        
        db.commit()
        db.refresh(workout)
        
        logger.info(f"Treino atualizado com sucesso!")
        return {"message": "Workout updated successfully", "data": workout}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
# Rota para deletar um treino
@router.delete("/workouts/{id}")
async def delete_workout(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Removendo treino com ID: {id}")
        workout = db.exec(select(Workout).where(Workout.id == id)).first()
        if workout is None:
            logger.warning(f"Treino com ID {id} nao encontrado")
            return {"error": "Workout not found"}
        
        db.delete(workout)
        db.commit()
        
        logger.info(f"Treino removido com sucesso!")
        return {"message": "Workout deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover um treino: {str(e)}")
        return {"error": str(e)}

# Rota para pegar treino pelo id
@router.get("/workouts/{id}")
async def get_workout(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Buscando treino com ID: {id}")
        workout = db.exec(select(Workout).where(Workout.id == id)).first()
        if workout is None:
            logger.warning(f"Treino com ID {id} nao encontrado")
            return {"error": "Workout not found"}
        
        logger.info(f"Treino encontrado: {workout}")
        return {"message": "Workout found successfully", "data": workout}
    except Exception as e:
        return {"error": str(e)}
    
# Rota para listar treinos
@router.get("/workouts")
async def get_workouts(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page (max 100)"),
    title: Optional[str] = Query(None, description="Filter by workout title"),
    description: Optional[str] = Query(None, description="Filter by workout description"),
    min_rest_time: Optional[int] = Query(None, description="Filter by minimum rest time"),
    max_rest_time: Optional[int] = Query(None, description="Filter by maximum rest time"),
    type: Optional[str] = Query(None, description="Filter by workout type"),
    category: Optional[str] = Query(None, description="Filter by workout category")
):
    try:
        logger.info(f"Buscando treinos...")
        filters = []
        if title:
            filters.append(Workout.title.ilike(f"%{title}%"))
        if description:
            filters.append(Workout.description.ilike(f"%{description}%"))
        if min_rest_time is not None:
            filters.append(Workout.rest_time >= min_rest_time)
        if max_rest_time is not None:
            filters.append(Workout.rest_time <= max_rest_time)
        if type:
            filters.append(Workout.type == type)
        if category:
            filters.append(Workout.category == category)

        offset = (page - 1) * limit
        stmt = select(Workout).where(and_(*filters)).offset(offset).limit(limit) if filters else select(Workout).offset(offset).limit(limit)
        workouts = db.exec(stmt).all()

        total_workouts = db.exec(select(func.count()).select_from(Workout).where(and_(*filters))).first() if filters else db.exec(select(func.count()).select_from(Workout)).first()
        total_pages = ceil(total_workouts / limit)
        
        if total_workouts > 0:
            logger.info(f"Encontrados {total_workouts} treinos")
        else:
            logger.info(f"Nenhum treino encontrado")

        return {
            "message": "Workouts found successfully",
            "data": workouts,
            "page": page,
            "limit": limit,
            "total_workouts": total_workouts,
            "total_pages": total_pages
        }
    except Exception as e:
        logger.error(f"Erro ao buscar treinos: {str(e)}")
        return {"error": str(e)}
    
# Rota para retorno da quantidade de treinos
@router.get("/quantity/workouts")
async def get_workouts_quantity(db: Session = Depends(get_db)):
    try:
        logger.info(f"Calculando quantidade de treinos...")
        quantity = db.exec(select(func.count()).select_from(Workout)).first()
        
        logger.info(f"Quantidade de treinos: {quantity}")
        return {"message": "Workouts quantity found successfully", "data": str(quantity)}
    except Exception as e:
        logger.error(f"Erro ao calcular a quantidade de treinos: {str(e)}")
        return {"error": str(e)}