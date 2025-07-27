from flask import Blueprint, request, jsonify
from app.models import Task, User
from app.schemas import TaskSchema
from app import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

tasks_bp = Blueprint('tasks', __name__)
tasks_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


#get all
@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    #data = request.get_json()
    id = get_jwt_identity()

    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    tasks = user.tasks
    return jsonify(tasks_schema.dump(tasks))

#create tasks
@tasks_bp.route('/create', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()

    if not data or not data.get('title'):
        return jsonify({'message': 'Título da tarefa é obrigatório'}), 400

    #cria nova task
    new_task = Task(
        title = data['title'],
        description=data.get('description'),
        status=data.get('status', 'pendente'),
        created_at=datetime.utcnow()
    )

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    #associa a task com o usuario
    new_task.users.append(user)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Tarefa criada com sucesso'}), 201