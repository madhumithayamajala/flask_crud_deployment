import json
from models import User
from settings import db
import pytest
from app import app as flask_app
import random
import string


def generate_random_email():
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'example.com']
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 10)))
    domain = random.choice(domains)
    return f"{username}@{domain}"


random_email = generate_random_email()


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def sample_user(app):
    with app.app_context():
        user = User(
            email=generate_random_email(),
            first_name="yamajala",
            last_name="madhumitha",
            password="Welcome@1234",
            mobile_number="9012390123"
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

    return user


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200


#
# def test_get_user(app, client, sample_user):
def test_get_user(app, client, sample_user):
    response = client.get(f"/user/{sample_user.id}")
    assert response.status_code == 200
    user_data = json.loads(response.data)
    assert user_data["data"]["first_name"] == "yamajala"
    assert user_data["data"]["last_name"] == "madhumitha"
    # assert user_data["data"]["email"] == generate_random_email()
    assert user_data["data"]["mobile_number"] == "9012390123"


def test_get_invalid_user(app, client):
    response = client.get(f"/user/867867678")
    assert response.status_code == 404
    user_data = json.loads(response.data)
    assert user_data["message"] == "User not found"
    assert user_data["status"] == "failed"


def test_create_user(app, client):
    new_user_data = {
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
        "email": random_email,
        "password": "NewPassword123",
        "mobile_number": "912345912345",
    }
    response = client.post("/user", json=new_user_data)
    assert response.status_code == 201
    created_user_data = json.loads(response.data)
    assert created_user_data["data"]["first_name"] == "NewFirstName"
    assert created_user_data["data"]["last_name"] == "NewLastName"
    assert created_user_data["data"]["email"] == random_email
    assert created_user_data["data"]["mobile_number"] == "912345912345"


def test_create_user_duplicate_email(app, client):
    new_user_data = {
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
        "email": random_email,
        "password": "NewPassword123",
        "mobile_number": "912345912345",
    }
    response = client.post("/user", json=new_user_data)
    assert response.status_code == 409
    created_user_data = json.loads(response.data)
    assert created_user_data["message"] == "Email already exists"


def test_create_user_check_invalid_email(app, client):
    new_user_data = {
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
        "email": "madhu",
        "password": "NewPassword123",
        "mobile_number": "912345912345",
    }
    response = client.post("/user", json=new_user_data)
    assert response.status_code == 400
    created_user_data = json.loads(response.data)
    assert created_user_data["error"] == "Invalid email address"


def test_create_user_check_without_email(app, client):
    new_user_data = {
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
        "password": "NewPassword123",
        "mobile_number": "912345912345",
    }
    response = client.post("/user", json=new_user_data)
    assert response.status_code == 400
    created_user_data = json.loads(response.data)
    assert created_user_data["error"] == "'email'"


def test_create_user_check_without_payload(app, client):
    new_user_data = {

    }
    response = client.post("/user", json=new_user_data)
    assert response.status_code == 400
    created_user_data = json.loads(response.data)
    assert created_user_data["message"] == "Empty payload received"


def test_update_user(app, client, sample_user):
    updated_data = {
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
        "email": generate_random_email(),
        "mobile_number": "9129129120",
    }
    response = client.put(f"/user/{sample_user.id}", json=updated_data)
    assert response.status_code == 200
    updated_response = client.get(f"/user/{sample_user.id}")
    updated_user_data = json.loads(updated_response.data)
    assert updated_user_data["data"]["first_name"] == "UpdatedFirstName"
    assert updated_user_data["data"]["last_name"] == "UpdatedLastName"
    assert updated_user_data["data"]["email"] != "updated_emails@example.com"
    assert updated_user_data["data"]["mobile_number"] == "9129129120"


def test_update_user_existing_email(app, client, sample_user):
    updated_data = {
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
        "email": random_email,
        "mobile_number": "9129129120",
    }
    response = client.put(f"/user/{sample_user.id}", json=updated_data)
    assert response.status_code == 409
    updated_user_data = json.loads(response.data)
    assert updated_user_data["message"] == "Email already exists"


def test_update_user_invalid_email(app, client, sample_user):
    updated_data = {
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
        "email": "ramu",
        "mobile_number": "9129129120",
    }
    response = client.put(f"/user/{sample_user.id}", json=updated_data)
    assert response.status_code == 400
    updated_user_data = json.loads(response.data)
    assert updated_user_data["error"] == "Invalid email address"


def test_delete_user(app, client, sample_user):
    response = client.delete(f"/user/{sample_user.id}")
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response["message"] == "User deleted successfully"
    deleted_response = client.get(f"/user/{sample_user.id}")
    assert deleted_response.status_code == 404
    deleted_user_data = json.loads(deleted_response.data)
    assert deleted_user_data["message"] == "User not found"
