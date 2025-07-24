from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from datetime import datetime, timedelta
from app.schemas import UserSchema
import jwt
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
    
    return jsonify({"message": "Usuário cadastrado com sucesso!"})
    
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
        
    #gerar token
    payload ={
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1) 
    }

    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token, 'username': user.username})








   