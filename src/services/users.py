from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, and_, select
from sqlalchemy.sql import func
from database import get_db
from models.user import User
from math import ceil
from services.configs import users_logger as logger

# Criar roteador
router = APIRouter()

# Rota para criar um novo usuário
@router.post("/users")
async def create_user(user: User, db: Session = Depends(get_db)):
    try:
        logger.info(f"Criando um novo usuário...")
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Usuário criado com sucesso!")
        return {"message": "User created successfully", "data": user}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar um novo usuário: {str(e)}")
        return {"error": str(e)}
    
# Rota para atualizar um usurário
@router.put("/users/{id}")
async def update_user(id: int, updated_user: User, db: Session = Depends(get_db)):
    try:
        logger.info(f"Atualizando usuário com ID: {id}")
        user = db.exec(select(User).where(User.id == id)).first()
        if user is None:
            logger.warning(f"Usuário com ID {id} não encontrado")
            return {"error": "User not found"}
        user.name = updated_user.name
        user.age = updated_user.age
        user.cpf = updated_user.cpf
        user.role = updated_user.role
        user.email = updated_user.email
        user.password = updated_user.password
        
        db.commit()
        db.refresh(user)
        logger.info(f"Usuário atualizado com sucesso!")
        return {"message": "User updated successfully", "data": user}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar um usuário: {str(e)}")
        return {"error": str(e)}
    
# Rota para deletar um usuário
@router.delete("/users/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Removendo usuário com ID: {id}")
        user = db.exec(select(User).where(User.id == id)).first()
        if user is None:
            logger.warning(f"Usuário com ID {id} não encontrado")
            return {"error": "User not found"}
        
        db.delete(user)
        db.commit()
        logger.info(f"Usuário removido com sucesso!")
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover um usuário: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# Rota para pegar usuário pelo id
@router.get("/users/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Buscando usuário com ID: {id}")
        user = db.exec(select(User).where(User.id == id)).first()
        if user is None:
            logger.warning(f"Usuário com ID {id} não encontrado")
            return {"error": "User not found"}
        
        logger.info(f"Usuário encontrado: {user}")
        return {"message": "User found successfully", "data": user}
    except Exception as e:
        return {"error": str(e)}
    
# Rota para listar usuários
@router.get("/users")
async def get_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page (max 100)"),
    name: Optional[str] = Query(None, description="Filter by user name"),
    min_age: Optional[int] = Query(None, description="Filter by minimum age"),
    max_age: Optional[int] = Query(None, description="Filter by maximum age"),
    role: Optional[str] = Query(None, description="Filter by user role")
):
    try:
        logger.info(f"Buscando usuários...")
        filters = []
        if name:
            filters.append(User.name.ilike(f"%{name}%"))
        if min_age is not None:
            filters.append(User.age >= min_age)
        if max_age is not None:
            filters.append(User.age <= max_age)
        if role:
            filters.append(User.role == role)
        
        offset = (page - 1) * limit
        stmt = select(User).where(and_(*filters)).offset(offset).limit(limit) if filters else select(User).offset(offset).limit(limit)
        users = db.exec(stmt).all()

        total_users = db.exec(select(func.count()).select_from(User).where(and_(*filters))).first() if filters else db.exec(select(func.count()).select_from(User)).first()
        total_pages = ceil(total_users / limit)
        
        if total_users > 0:
            logger.info(f"Usuários encontrados com sucesso!")
        else:
            logger.warning(f"Nenhum usuário encontrado!")
            
        return {
            "message": "Users found successfully",
            "data": users,
            "page": page,
            "limit": limit,
            "total_users": total_users,
            "total_pages": total_pages
        }
    except Exception as e:
        return {"error": str(e)}
    
# Rota para retorno da quantidade de usuários
@router.get("/quantity/users")
async def get_users_quantity(db: Session = Depends(get_db)):
    try:
        logger.info(f"Calculando quantidade de usuários...");
        quantity = db.exec(select(func.count()).select_from(User)).first()
        
        logger.info(f"Quantidade de usuários encontrados: {quantity}");
        return {"message": "Users quantity found successfully", "data": str(quantity)}
    except Exception as e:
        return {"error": str(e)}