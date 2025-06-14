from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @property
    def is_complete(self):
        return self.completed_at is not None
    
    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.is_complete
        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id
        return task_as_dict
    
    @classmethod
    def from_dict(cls, task_data):

        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at = task_data.get("completed_at", None),
            goal_id=task_data.get("goal_id", None)
        )
        
    