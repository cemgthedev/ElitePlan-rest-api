# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from database import get_db
from models.user import User

# Criar roteador
router = APIRouter()

# Rota para criar um novo usuário
@router.post("/users")
async def create_user(user: User, db: Session = Depends(get_db)):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User created successfully", "data": user}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
# Rota para pegar usuário pelo id
@router.get("/users/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.exec(select(User).where(User.id == id)).first()
        if user is None:
            return {"error": "User not found"}
        return {"message": "User found successfully", "data": user}
    except Exception as e:
        return {"error": str(e)}