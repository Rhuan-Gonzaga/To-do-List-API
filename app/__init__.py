from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .config import Config

# Inicialização sem passar o app aqui
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa as extensões com o app criado
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Importa os modelos aqui para que o Flask-Migrate os detecte
    from app.models import User, Task  # certifique-se de que os modelos estão corretos

    from app.views.tasks import tasks_bp
    from app.views.users import users_bp
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    return app
