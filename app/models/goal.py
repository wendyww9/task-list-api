from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self, include_tasks=False):
        goal_dict = {
            "id": self.id,
            "title": self.title
        }

        if include_tasks:
            goal_dict["tasks"] = [task.to_dict() for task in self.tasks] 

        return goal_dict  
    
    @classmethod
    def from_dict(cls, goal_data):
        return cls(title=goal_data["title"])
        
    def update_goal(self, response_body):
        if "id" in response_body:
            self.id = response_body["id"]
        if "title" in response_body:
            self.title = response_body["title"]
        if "tasks" in response_body:
            self.tasks = response_body["tasks"]
        