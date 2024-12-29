from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

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
    plans: list["PlanWorkouts"] = Relationship(back_populates="workout")
    exercices: list["WorkoutExercices"] = Relationship(back_populates="workout")