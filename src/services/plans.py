# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy.sql import func
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
    
# Rota para atualizar um plano
@router.put("/plans/{id}")
async def update_plan(id: int, updated_plan: Plan, db: Session = Depends(get_db)):
    try:
        plan = db.exec(select(Plan).where(Plan.id == id)).first()
        if plan is None:
            return {"error": "Plan not found"}
        plan.title = updated_plan.title
        plan.description = updated_plan.description
        plan.type = updated_plan.type
        plan.category = updated_plan.category
        plan.price = updated_plan.price
        
        db.commit()
        db.refresh(plan)
        return {"message": "Plan updated successfully", "data": plan}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
# Rota para deletar um plano
@router.delete("/plans/{id}")
async def delete_plan(id: int, db: Session = Depends(get_db)):
    try:
        plan = db.exec(select(Plan).where(Plan.id == id)).first()
        if plan is None:
            return {"error": "Plan not found"}
        
        db.delete(plan)
        db.commit()
        return {"message": "Plan deleted successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
# Rota para pegar plano pelo id
@router.get("/plans/{id}")
async def get_plan(id: int, db: Session = Depends(get_db)):
    try:
        plan = db.exec(select(Plan).where(Plan.id == id)).first()
        if plan is None:
            return {"error": "Plan not found"}
        return {"message": "Plan found successfully", "data": plan}
    except Exception as e:
        return {"error": str(e)}
    
# Rota para listar planos
@router.get("/plans")
async def get_plans(db: Session = Depends(get_db)):
    try:
        plans = db.exec(select(Plan)).all()
        return {"message": "Plans found successfully", "data": plans}
    except Exception as e:
        return {"error": str(e)}
    
# Rota para retorno da quantidade de planos
@router.get("/quantity/plans")
async def get_plans_quantity(db: Session = Depends(get_db)):
    try:
        quantity = db.exec(select(func.count()).select_from(Plan)).first()
        return {"message": "Plans quantity found successfully", "data": str(quantity)}
    except Exception as e:
        return {"error": str(e)}