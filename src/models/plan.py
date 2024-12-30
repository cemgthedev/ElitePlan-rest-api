from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from user_plans import UserPlans
    from plan_workouts import PlanWorkouts

# Plan Entity
class Plan(SQLModel, table=True):
    __tablename__ = "plans"  # Table name
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    type: str
    category: str
    price: float
    users: List["UserPlans"] = Relationship(back_populates="plan", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    workouts: List["PlanWorkouts"] = Relationship(back_populates="plan", sa_relationship_kwargs={"cascade": "all, delete-orphan"})