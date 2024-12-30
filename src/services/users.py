# Criar roteador
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy.sql import func
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
    
# Rota para atualizar um usurário
@router.put("/users/{id}")
async def update_user(id: int, updated_user: User, db: Session = Depends(get_db)):
    try:
        user = db.exec(select(User).where(User.id == id)).first()
        if user is None:
            return {"error": "User not found"}
        user.name = updated_user.name
        user.age = updated_user.age
        user.cpf = updated_user.cpf
        user.role = updated_user.role
        user.email = updated_user.email
        user.password = updated_user.password
        
        db.commit()
        db.refresh(user)
        return {"message": "User updated successfully", "data": user}
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
    
# Rota para listar usuários
@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.exec(select(User)).all()
        return {"message": "Users found successfully", "data": users}
    except Exception as e:
        return {"error": str(e)}
    
# Rota para retorno da quantidade de usuários
@router.get("/quantity/users")
async def get_users_quantity(db: Session = Depends(get_db)):
    try:
        quantity = db.exec(select(func.count()).select_from(User)).first()
        return {"message": "Users quantity found successfully", "data": str(quantity)}
    except Exception as e:
        return {"error": str(e)}