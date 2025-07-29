import pytest
from flask import Flask
from app import create_app, db
from app.models import User
from flask_jwt_extended import create_access_token
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "testsecret",
        "JWT_SECRET_KEY": "testjwtsecret",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(app):
    with app.app_context():
        user = User(username="testuser", password_hash="1234")
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.id)
        return token
