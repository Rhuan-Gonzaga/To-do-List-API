from datetime import datetime
from app import db

# Tabela associativa entre users e tasks
user_tasks = db.Table(
    'user_tasks',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), primary_key=True)
)

# Modelo User
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com tarefas
    tasks = db.relationship(
        'Task',
        secondary=user_tasks,
        back_populates='users'
    )

# Modelo Task
class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('pendente', 'em andamento', 'concluída'), default='pendente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com usuários
    users = db.relationship(
        'User',
        secondary=user_tasks,
        back_populates='tasks'
    )
