from flask import Blueprint, request, jsonify
from app.models import Task, User
from app.schemas import TaskSchema
from app import db
from datetime import datetime, timezone
from flask_jwt_extended import jwt_required, get_jwt_identity

tasks_bp = Blueprint('tasks', __name__)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


#get all
@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    #data = request.get_json()
    id = get_jwt_identity()

    user = db.session.get(User, id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    tasks = user.tasks
    return jsonify(tasks_schema.dump(tasks))

#get user task by id
@tasks_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_tasks_id(id):

    user_id = get_jwt_identity()
   

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    tasks = Task.query.join(Task.users).filter(Task.id == id, User.id == user_id).first()
    
    if not tasks:
        return jsonify({'message': 'Tarefa não encontrada ou não pertence a este usuário'}), 404
   
    return jsonify(task_schema.dump(tasks)), 200


#get user task by status
@tasks_bp.route('/status/<string:status>', methods=['GET'])
@jwt_required()
def get_tasks_status(status):

    user_id = get_jwt_identity()
   
    status_permitidos = ['pendente', 'em andamento', 'concluída']
    if status not in status_permitidos:
        return jsonify({'message': 'Status inválido. Use: pendente, em andamento ou concluída.'}), 400
    
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    tasks = Task.query.join(Task.users).filter(Task.status == status, User.id == user_id).all()
    
    if not tasks:
        return jsonify({'message': 'Tarefa não encontrada ou não pertence a este usuário'}), 404
   
    return jsonify(tasks_schema.dump(tasks)), 200

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
        created_at=datetime.now(timezone.utc)
    )

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    #associa a task com o usuario
    new_task.users.append(user)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Tarefa criada com sucesso'}), 201

@tasks_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    user_id = get_jwt_identity()
    data = request.json

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    task = Task.query.join(Task.users).filter(Task.id == id, User.id == user_id).first()
    if not task:
        return jsonify({'message': 'Tarefa não encontrada ou não pertence a este usuário'}), 404
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)

    db.session.commit()
    return jsonify({'message': 'Tarefa atualizada'}), 200

@tasks_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    task = Task.query.join(Task.users).filter(Task.id == id, User.id == user_id).first()
    if not task:
        return jsonify({'message': 'Tarefa não encontrada ou não pertence a este usuário'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Tarefa deletada com sucesso'}), 200
   