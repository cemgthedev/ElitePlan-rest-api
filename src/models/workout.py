from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from plan_workouts import PlanWorkouts
    from workout_exercices import WorkoutExercices

# Workout Entity
class Workout(SQLModel, table=True):
    __tablename__ = "workouts"  # Table name
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    rest_time: int
    type: str
    category: str
    plans: List["PlanWorkouts"] = Relationship(back_populates="workout", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    exercices: List["WorkoutExercices"] = Relationship(back_populates="workout", sa_relationship_kwargs={"cascade": "all, delete-orphan"})