from flask import Flask, request, jsonify
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from settings import db, app, migrate
from models import User
from user_schema import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.errorhandler(Exception)
def handle_error(error):
    response = {"status": "error", "message": "An unexpected error occurred"}
    return jsonify(response), 500

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.order_by(desc(User.created_at)).all()
        serialized_users = users_schema.dump(users)
        response = {"status": "success", "data": serialized_users, "message": "Users fetched successfully"}
        return jsonify(response)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "failed", "message": "Database error occurred", "error": str(e)}), 500

@app.route('/user/<int:id>', methods=['GET'])
def get_specific_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"status": "failed", "message": "User not found"}), 404
        serialized_user = user_schema.dump(user)
        response = {"status": "success", "data": serialized_user, "message": "User fetched successfully"}
        return jsonify(response)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "failed", "message": "Database error occurred", "error": str(e)}), 500

@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "failed", "message": "Empty payload received"}), 400

        errors = user_schema.validate(data)
        if errors:
            return jsonify({"status": "failed", "message": f"Validation errors {errors}"}), 400
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"status": "failed", "message": "Email already exists"}), 409

        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        serialized_user = user_schema.dump(new_user)
        response_data = {"data": serialized_user, "status": "success", "message": "User created successfully"}
        return jsonify(response_data), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "failed", "message": "Database error occurred", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "failed", "message": "An error occurred", "error": str(e)}), 400

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"status": "failed", "message": "User not found"}), 404
        data = request.get_json()
        errors = user_schema.validate(data, partial=True)
        if errors:
            return jsonify({"status": "failed", "message": "Validation errors", "errors": errors}), 400

        updated_email = data.get("email")
        if updated_email and updated_email != user.email:
            existing_user = User.query.filter_by(email=updated_email).first()
            if existing_user:
                return jsonify({"status": "failed", "message": "Email already exists"}), 409

        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.password = data.get("password", user.password)
        user.mobile_number = data.get("mobile_number", user.mobile_number)
        db.session.commit()
        serialized_user = user_schema.dump(user)
        response_data = {"data": serialized_user, "status": "success", "message": "User updated successfully"}
        return jsonify(response_data), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "failed", "message": "Database error occurred", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "failed", "message": "An error occurred", "error": str(e)}), 400

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"status": "failed", "message": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        response_data = {"data": {}, "status": "success", "message": "User deleted successfully"}
        return jsonify(response_data), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "failed", "message": "Database error occurred", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "failed", "message": "An error occurred", "error": str(e)}), 400

if __name__ == "__main__":
    app.run()
