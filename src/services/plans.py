# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_db
from models.plan import Plan

# Criar roteador
router = APIRouter()

# Rota para criar um novo plano
@router.post("/plans")
async def create_plan(plan: Plan, db: Session = Depends(get_db)):
    try:
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return {"message": "Plan created successfully", "data": plan}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}