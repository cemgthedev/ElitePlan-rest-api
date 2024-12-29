from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from workout_exercices import WorkoutExercices

# Exercice Entity
class Exercice(SQLModel, table=True):
    __tablename__ = "exercices"  # Table name
    id: int = Field(default=None, primary_key=True)
    title: str
    n_sections: int
    n_reps: int
    weight: float
    tutorial_url: str
    workouts: list["WorkoutExercices"] = Relationship(back_populates="exercice")