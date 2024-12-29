# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy.sql import func
from database import get_db
from models.exercice import Exercice

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
async def get_exercices(db: Session = Depends(get_db)):
    try:
        exercices = db.exec(select(Exercice)).all()
        return {"message": "Exercices found successfully", "data": exercices}
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