from flask import Blueprint, abort, make_response, Response, request
from ..db import db
from app.models.goal import Goal
from .route_utilities import validate_model
import requests
import json
import os

bp = Blueprint("goals_bp",__name__,url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError as e:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_goal)
    db.session.commit()

    return {"goal":new_goal.to_dict()}, 201

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

