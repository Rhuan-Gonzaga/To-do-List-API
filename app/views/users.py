from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.schemas import UserSchema
from app import db

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_bp.route('/signup', methods=['POST'])
def create_user():
    data = request.json

    user = User(
        username = data['username'],
        password_hash = generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "Usuário cadastrado com sucesso!"})
    









   