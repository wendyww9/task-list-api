from flask import Blueprint, Response, request
from ..db import db
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model, create_model_response


bp = Blueprint("goals_bp",__name__,url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model_response(Goal, request_body, "goal")


@bp.post("/<goal_id>/tasks")
def post_task_id_to_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    task_ids = request_body.get("task_ids")

    goal.tasks = []
    tasks = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
        tasks.append(task)

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in tasks]
    }


@bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query)

    goals_response = [goal.to_dict() for goal in goals]
    
    return goals_response


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}


@bp.get("/<goal_id>/tasks")
def get_all_goal_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict(include_tasks=True)


@bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.update_goal(request_body)
    db.session.commit()

    return Response(status=204, mimetype ="application/json")


@bp.delete("/<goal_id>")
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype ="application/json")
