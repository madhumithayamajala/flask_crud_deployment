from flask import Flask, request, jsonify
from sqlalchemy.orm import class_mapper

from settings import db, app, migrate
from models import User
from flask_migrate import Migrate


@app.route('/user', methods=['GET'])
def get_all_users():
    """
    This function is mapped to the /user endpoint and
    it renders all user records using the GET HTTP method.
    """
    message = {
        'status': 404,
        'message': 'No users found'
    }

    users = User.query.all()

    # Convert user objects to a list of dictionaries
    data_list = [
        {column.name: getattr(user, column.name) for column in class_mapper(user.__class__).mapped_table.columns}
        for user in users
    ]

    message.update({
        'status': 200,
        'message': 'All records are fetched',
        'data': data_list
    })

    return jsonify(message)


@app.route('/user/<int:id>', methods=['GET'])
def get_specific_user(id):
    """
    this function is map with /user/pk endpoint and 
    it render specific user records with respect to its pk 
    using GET Http method
    """
    message = {
        'status': 404,
        'message': 'User not exists'
    }

    user = User.query.filter_by(id=id).first()

    if user is None:
        return jsonify(message)

    # Convert user object to dictionary
    data_dict = {column.name: getattr(user, column.name) for column in
                 class_mapper(user.__class__).mapped_table.columns}

    message.update({
        'status': 200,
        'message': 'Record are fetched',
        'data': data_dict
    })

    return jsonify(message)

@app.route('/user', methods=['POST'])
def create_user():
    """
    this function is map with /user endpoint and 
    it create user records using POST Http method
    """
    message = {
        'status': 404,
        'message': 'Something went wrong'
    }
    try:
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        mobile_number = request.form.get('mobile_number', '').strip()

        if not first_name or not last_name or not email or not password or not mobile_number:
            missing_fields = []
            if not first_name:
                missing_fields.append('first_name')
            if not last_name:
                missing_fields.append('last_name')
            if not email:
                missing_fields.append('email')
            if not password:
                missing_fields.append('password')
            if not mobile_number:
                missing_fields.append('mobile_number')

            message['message'] = f'Required fields are missing: {", ".join(missing_fields)}'
            return jsonify(message), 400
    
    # Check if email already exists
        if User.query.filter_by(email=email).first() is not None:
            message['message'] = 'Email already exists. Please use a different email.'
            return jsonify(message), 400

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            mobile_number=mobile_number
        )

        db.session.add(user)
        db.session.commit()

        data_dict = {column.name: getattr(user, column.name) for column in
                 class_mapper(user.__class__).mapped_table.columns}

        message.update({
            'status': 201,
            'message': 'User created successfully!!! ',
            'user_id': user.id,
            'data':data_dict
        })
    except Exception as e:
        message['message'] = f'Something went wrong {e}'

    resp = jsonify(message)
    return resp


@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    """
    this function is map with /user/pk endpoint and 
    it update specific user records using PUT Http method
    """
    message = {
        'status': 404,
        'message': 'user not found'
    }
    try:
        new_first_name = request.form.get('first_name', None)
        new_last_name = request.form.get('last_name', None)
        new_email = request.form.get('email', None)
        new_password = request.form.get('password', None)
        new_mobile_number = request.form.get('mobile_number', None)
        try:
            current_user = User.query.get_or_404(id)
        except:
            return jsonify(message)

        # Email validation
        if new_email:
            # Check if the new email is already associated with another user
            if User.query.filter(User.id != id, User.email == new_email).first() is not None:
                message['message'] = 'Email is already associated with another user.'
                return jsonify(message), 400

            current_user.email = new_email

        if new_email:
            current_user.email = new_email
        if new_first_name:
            current_user.first_name = new_first_name
        if new_last_name:
            current_user.last_name = new_last_name
        if new_password:
            current_user.password = new_password
        if new_mobile_number:
            current_user.mobile_number = new_mobile_number

        db.session.commit()
        message.update({
            'status': 200,
            'message': 'User details updated successfully!!! '
        })
    except:
        pass
    resp = jsonify(message)
    return resp


@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    this function is map with /user/pk endpoint and 
    it delete specific user records using DELETE Http method
    """
    message = {
        'status': 404,
        'message': 'user not found'
    }
    try:
        current_user = User.query.get_or_404(id)
        db.session.delete(current_user)
        db.session.commit()
        message.update({
            'status': 200,
            'message': 'user record delete successfully!!! '
        })
    except:
        pass
    resp = jsonify(message)
    return resp


if __name__ == "__main__":
    migrate.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
