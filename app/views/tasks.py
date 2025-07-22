from flask import Blueprint, request, jsonify
from app.models import Task
from app.schemas import TaskSchema
from app import db

tasks_bp = Blueprint('tasks', __name__)
tasks_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify(tasks_schema.dump(tasks))
