from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from workout import Workout
    from exercice import Exercice

# WorkoutExercices Entity
class WorkoutExercices(SQLModel, table=True):
    __tablename__ = "workout_exercices"  # Table name
    id: int = Field(default=None, primary_key=True)
    workout_id: int = Field(foreign_key="workouts.id")  # Foreign Key for Workout
    exercice_id: int = Field(foreign_key="exercices.id")    # Foreign Key for Exercice
    created_at: datetime = Field(default_factory=datetime.now)
    workout: "Workout" = Relationship(back_populates="exercices")
    exercice: "Exercice" = Relationship(back_populates="workouts")