from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plan_workouts import PlanWorkouts
    from workout_exercices import WorkoutExercice

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
    exercises: list["WorkoutExercice"] = Relationship(back_populates="workout")