from fastapi import FastAPI, Depends
from sqlmodel import Session
from database import get_db
from models import *
from services.users import router as users_router
from services.exercices import router as exercices_router
from services.workouts import router as workouts_router
from services.plans import router as plans_router
from services.workout_exercices import router as workout_exercices_router

app = FastAPI()

@app.get("/")
def get_db(db: Session = Depends(get_db)):
    if db is None:
        return {"message": "Database not connected"}
    return {"message": "Database connected"}

# Adicionando rotas de usuários
app.include_router(users_router)

# Adicionando rotas de exercícios
app.include_router(exercices_router)

# Adicionando rotas de treinos
app.include_router(workouts_router)

# Adicionando rotas de planos
app.include_router(plans_router)

# Adicionando rotas de exercícios para treinos
app.include_router(workout_exercices_router)