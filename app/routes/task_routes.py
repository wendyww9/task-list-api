from flask import Blueprint, request, Response, abort, make_response
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model
from datetime import datetime
import requests
import json
import os

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)

    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    sort_order = request.args.get("sort")
    if sort_order == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_order == "desc":
        query = query.order_by(Task.title.desc())
 
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return tasks_response, 200

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    
    return {"task": task.to_dict()}


@bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.title = request_body['title']
    task.description = request_body['description']
    
    db.session.commit()
    db.session.commit()

    return Response(status=204, mimetype ="application/json")

@bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype ="application/json")
    
@bp.patch("/<task_id>/mark_complete")
def update_one_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    
    db.session.commit()
    db.session.commit()
    call_slack_api(task.title)

    return Response(status=204, mimetype ="application/json")

def call_slack_api(title):
    url = "https://slack.com/api/chat.postMessage"

    payload = json.dumps({
    "channel": "test-slack-api",
    "text": f"Someone just completed the task {title}"
    })

    headers = {
    'Authorization': f"Bearer {os.environ.get('SLACK_Bot_User_OAuth_Token')}",
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return None


@bp.patch("/<task_id>/mark_incomplete")
def update_one_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    
    db.session.commit()
    db.session.commit()

    return Response(status=204, mimetype ="application/json")  