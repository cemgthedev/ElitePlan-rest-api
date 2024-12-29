# Criar roteador
from fastapi import APIRouter, Depends
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