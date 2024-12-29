# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session

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
        return {"message": "Exercice created successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}