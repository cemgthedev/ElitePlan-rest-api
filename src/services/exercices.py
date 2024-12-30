# Criar roteador
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.sql import func
from database import get_db
from models.exercice import Exercice
from math import ceil

# Criar roteador
router = APIRouter()

# Rota para criar um novo exercício
@router.post("/exercices")
async def create_exercice(exercice: Exercice, db: Session = Depends(get_db)):
    try:
        db.add(exercice)
        db.commit()
        db.refresh(exercice)
        return {"message": "Exercice created successfully", "data": exercice}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
# Rota para atualizar um exercício
@router.put("/exercices/{id}")
async def update_exercice(id: int, updated_exercice: Exercice, db: Session = Depends(get_db)):
    try:
        exercice = db.exec(select(Exercice).where(Exercice.id == id)).first()
        if exercice is None:
            return {"error": "Exercice not found"}
        exercice.title = updated_exercice.title
        exercice.n_sections = updated_exercice.n_sections
        exercice.n_reps = updated_exercice.n_reps
        exercice.weight = updated_exercice.weight
        exercice.tutorial_url = updated_exercice.tutorial_url
        
        db.commit()
        db.refresh(exercice)
        return {"message": "Exercice updated successfully", "data": exercice}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

# Rota para deletar um exercício
@router.delete("/exercices/{id}")
async def delete_exercice(id: int, db: Session = Depends(get_db)):
    try:
        exercice = db.exec(select(Exercice).where(Exercice.id == id)).first()
        if exercice is None:
            return {"error": "Exercice not found"}
        
        db.delete(exercice)
        db.commit()
        return {"message": "Exercice deleted successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
# Rota para pegar exercício pelo id
@router.get("/exercices/{id}")
async def get_exercice(id: int, db: Session = Depends(get_db)):
    try:
        exercice = db.exec(select(Exercice).where(Exercice.id == id)).first()
        if exercice is None:
            return {"error": "Exercice not found"}
        return {"message": "Exercice found successfully", "data": exercice}
    except Exception as e:
        return {"error": str(e)}
    
# Rota para listar exercícios
@router.get("/exercices")
async def get_exercices(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, ge=1, description="Number of results per page")
):
    try:
        offset = (page - 1) * limit
        stmt = select(Exercice).offset(offset).limit(limit)
        exercices = db.exec(stmt).all()

        total_exercices = db.exec(select(func.count()).select_from(Exercice)).first()
        total_pages = ceil(total_exercices / limit)

        return {
            "message": "Exercices found successfully",
            "data": exercices,
            "page": page,
            "limit": limit,
            "total_users": total_exercices,
            "total_pages": total_pages
        }
    except Exception as e:
        return {"error": str(e)}
    
# Rota para retorno da quantidade de exercícios
@router.get("/quantity/exercices")
async def get_exercices_quantity(db: Session = Depends(get_db)):
    try:
        quantity = db.exec(select(func.count()).select_from(Exercice)).first()
        return {"message": "Exercices quantity found successfully", "data": str(quantity)}
    except Exception as e:
        return {"error": str(e)}