from math import ceil
from fastapi import APIRouter, Depends, Query
from sqlalchemy.sql import func
from sqlmodel import Session, select
from datetime import datetime
from database import get_db
from models.user import User
from models.plan import Plan
from models.user_plans import UserPlans

# Criar roteador
router = APIRouter()

# Rota para adicionar um plano a um usuário
@router.post("/user_plans")
async def create_user_plan(user_plan: UserPlans, db: Session = Depends(get_db)):
    try:
        user = db.exec(select(User).where(User.id == user_plan.user_id)).first()
        if user is None:
            return {"error": "User not found"}
        
        plan = db.exec(select(Plan).where(Plan.id == user_plan.plan_id)).first()
        if plan is None:
            return {"error": "Plan not found"}
        
        user_plan.created_at = datetime.now()
        
        db.add(user_plan)
        db.commit()
        db.refresh(user_plan)
        return {"message": "Plan added to user successfully", "data": user_plan}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
# Rota para deletar um plano de um usuário
@router.delete("/user_plans/{id}")
async def delete_user_plan(id: int, db: Session = Depends(get_db)):
    try:
        user_plan = db.exec(select(UserPlans).where(UserPlans.id == id)).first()
        if user_plan is None:
            return {"error": "User plan not found"}
        
        db.delete(user_plan)
        db.commit()
        return {"message": "User plan deleted successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
# Rota para pegar um plano de um usuário pelo id
@router.get("/user_plans/{id}")
async def get_user_plan(id: int, db: Session = Depends(get_db)):
    try:
        user_plan = db.exec(select(UserPlans).where(UserPlans.id == id)).first()
        if user_plan is None:
            return {"error": "User plan not found"}
        return {"message": "User plan found successfully", "data": user_plan}
    except Exception as e:
        return {"error": str(e)}
    
# Rota para listar planos para usuários
@router.get("/user_plans")
async def get_user_plans(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page (max 100)")
):
    try:
        offset = (page - 1) * limit
        stmt = select(UserPlans).offset(offset).limit(limit)
        user_plans = db.exec(stmt).all()

        total_user_plans = db.exec(select(func.count()).select_from(UserPlans)).first()
        total_pages = ceil(total_user_plans / limit)

        return {
            "message": "User plans found successfully",
            "data": user_plans,
            "page": page,
            "limit": limit,
            "total_user_plans": total_user_plans,
            "total_pages": total_pages
        }
    except Exception as e:
        return {"error": str(e)}
    
# Rota para retorno da quantidade de planos para usuários
@router.get("/quantity/user_plans")
async def get_user_plans_quantity(db: Session = Depends(get_db)):
    try:
        quantity = db.exec(select(func.count()).select_from(UserPlans)).first()
        return {"message": "User plans quantity found successfully", "data": str(quantity)}
    except Exception as e:
        return {"error": str(e)}