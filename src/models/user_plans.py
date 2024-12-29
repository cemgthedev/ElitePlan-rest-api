from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user import User
    from plan import Plan

# UserPlans Entity
class UserPlans(SQLModel, table=True):
    __tablename__ = "user_plans"  # Table name
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")  # Foreign Key for User
    plan_id: int = Field(foreign_key="plans.id")  # Foreign Key for Plan
    created_at: datetime = Field(default_factory=datetime.now)
    user: "User" = Relationship(back_populates="plans")
    plan: "Plan" = Relationship(back_populates="users")