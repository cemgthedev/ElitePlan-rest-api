from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plan import Plan
    from workout import Workout

# PlanWorkouts Entity
class PlanWorkouts(SQLModel, table=True):
    __tablename__ = "plan_workouts"  # Table name
    id: int = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plans.id")        # Foreign Key for Plan
    workout_id: int = Field(foreign_key="workouts.id")  # Foreign Key for Workout
    created_at: datetime = Field(default_factory=datetime.now)
    plan: "Plan" = Relationship(back_populates="workouts")
    workout: "Workout" = Relationship(back_populates="plans")