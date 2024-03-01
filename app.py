from flask import request
from sqlalchemy import desc

from settings import db, app, migrate
from models import User

from user_schema import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/user', methods=['GET'])
def get_all_users():
    """
    This function is mapped to the /user endpoint and
    it renders all user records using the GET HTTP method.
    """
    users = User.query.order_by(desc(User.created_at)).all()
    serialized_users = users_schema.dump(users)
    response = {"status": "success", "data": serialized_users, "message": "Users fetched successfully"}
    return response


@app.route('/user/<int:id>', methods=['GET'])
def get_specific_user(id):
    """
    this function is map with /user/pk endpoint and 
    it render specific user records with respect to its pk 
    using GET Http method
    """
    user = db.session.get(User, id)
    if not user:
        return {"status": "failed", "message": "User not found"}, 404
    serialized_users = user_schema.dump(user)
    response = {"status": "success", "data": serialized_users, "message": "User fetched successfully"}
    return response


@app.route('/user', methods=['POST'])
def create_user():
    """
    this function is map with /user endpoint and 
    it create user records using POST Http method
    """
    try:
        data = request.get_json()
        if not data:
            return {"status": "failed", "message": "Empty payload received"}, 400

        errors = user_schema.validate(data)
        if errors:
            return {"status": "failed", "message": f"Validation errors {errors}"}, 400
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {"status": "failed", "message": "Email already exists"}, 409
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        serialized_user = user_schema.dump(new_user)
        response_data = {"data": serialized_user, "status": "success", "message": "User created successfully"}
        return response_data, 201

    except Exception as e:
        return {"status": "failed", "message": "An error occurred", "error": f"{str(e)}"}, 400


@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    """
    this function is map with /user/pk endpoint and 
    it update specific user records using PUT Http method
    """
    try:
        user = db.session.get(User, id)
        if not user:
            return {"status": "failed", "message": "User not found"}, 404
        data = request.get_json()
        errors = user_schema.validate(data, partial=True)
        if errors:
            return {"status": "failed", "message": "Validation errors", "errors": errors}, 400
        updated_email = data.get("email")
        if updated_email and updated_email != user.email:
            existing_user = User.query.filter_by(email=updated_email).first()
            if existing_user:
                return {"status": "failed",
                        "message": "Email already exists"}, 409  # Conflict status code for existing resource

        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.password = data.get("password", user.password)
        user.mobile_number = data.get("mobile_number", user.mobile_number)
        db.session.commit()
        serialized_user = user_schema.dump(user)
        response_data = {"data": serialized_user, "status": "success", "message": "User updated successfully"}
        return response_data, 200
    except Exception as e:
        return {"status": "failed", "message": "An error occurred", "error": str(e)}, 400


@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    this function is map with /user/pk endpoint and 
    it delete specific user records using DELETE Http method
    """
    try:
        user = db.session.get(User, id)
        if not user:
            return {"status": "failed", "message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        response_data = {"data": {}, "status": "success", "message": "User deleted successfully"}
        return response_data, 200
    except Exception as e:
        return {"status": "failed", "message": "An error occurred", "error": str(e)}, 500


# if __name__ == "__main__":
#     migrate.init_app(app)
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
if __name__ == "__main__":
    app.run()
