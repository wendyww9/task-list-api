from flask import Blueprint, abort, make_response, Response, request
from ..db import db
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model, create_model
import requests
import json
import os

bp = Blueprint("goals_bp",__name__,url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    data, status_code = create_model(Goal, request_body)
    return {"goal": data}, status_code

@bp.post("/<goal_id>/tasks")
def create_task_with_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    task_ids = request_body.get("task_ids")
    if not isinstance(task_ids, list):
        abort(make_response({"details": "Invalid data: 'task_ids' must be a list"}, 400))

    for task in goal.tasks:
        task.goal_id = None
    
    tasks = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
        tasks.append(task)

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in tasks]
    }, 200

@bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return goals_response, 200


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return {"goal": goal.to_dict()}

@bp.get("/<goal_id>/tasks")
def get_all_goal_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = [task.to_dict() for task in goal.tasks]

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks
    }, 200


@bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body['title']
    
    db.session.commit()
    db.session.commit()

    return Response(status=204, mimetype ="application/json")

@bp.delete("/<goal_id>")
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype ="application/json")

