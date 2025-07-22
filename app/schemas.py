from marshmallow import Schema, fields

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow import fields

from app.models import User, Task


class TaskSchema(SQLAlchemySchema):
    class Meta:
        model = Task
        load_instance = True
        include_relationships = True

    id = auto_field()
    title = auto_field()
    description = auto_field()
    status = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    users = fields.List(fields.Nested(lambda: UserSchema(only=("id", "username"))))


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

    id = auto_field()
    username = auto_field()
    created_at = auto_field()
    tasks = fields.List(fields.Nested(lambda: TaskSchema(only=("id", "title", "status"))))
