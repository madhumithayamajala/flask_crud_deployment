from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
