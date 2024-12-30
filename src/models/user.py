from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from user_plans import UserPlans

# User Entity
class User(SQLModel, table=True):
    __tablename__ = "users"  # Table name
    id: int = Field(default=None, primary_key=True)
    name: str
    age: Optional[int]
    cpf: str
    role: str
    email: str
    password: str
    plans: List["UserPlans"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})