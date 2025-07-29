from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from datetime import datetime, timedelta
from app.schemas import UserSchema
from flask_jwt_extended import create_access_token
from app import db

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_bp.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json()

    user = User(
        username = data['username'],
        password_hash = generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
    
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    #Verifica se o campo da request é vazio
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Usuário e senha são obrigatórios'}), 400
    
    #retorna o usuario
    user = User.query.filter_by(username=data['username']).first()

    #verificando se a senha do usuario é igual a do banco
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Usuário ou senha inválidos'}), 401
        
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    
    return jsonify({'token': access_token, 'username': user.username}), 200







   