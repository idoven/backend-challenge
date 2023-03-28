from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_access_token(client, username, password):
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    return response.json()["access_token"]

# Test registration
def test_register_admin():
    response = client.post(
        "/register",
        json={"username": "admin", "password": "admin123", "is_admin": True}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

def test_register_non_admin():
    response = client.post(
        "/register",
        json={"username": "user1", "password": "password123", "is_admin": False}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Only admin users can create new users"}

def test_register_existing_user():
    response = client.post(
        "/register",
        json={"username": "admin", "password": "admin123", "is_admin": True}
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Username already exists"}

# Test authentication
def test_authenticate_admin():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_authenticate_non_admin():
    response = client.post(
        "/token",
        data={"username": "user1", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_authenticate_invalid_credentials():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

# Test saving and retrieving data
def test_save_data_admin():
    access_token = get_access_token(client, "admin", "admin123")
    response = client.post(
        "/send_data",
        json={"data": {"foo": "bar"}},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin users are not allowed to save data"}

def test_save_data_non_admin():
    access_token = get_access_token(client, "user1", "password123")
    response = client.post(
        "/send_data",
        json={"data": {"foo": "bar"}},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Data saved successfully"}

def test_get_data_no_data():
    access_token = get_access_token(client, "user1", "password123")
    response = client.get(
        "/get_data",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "No data found for the user"}

def test_get_data_with_data():
    access_token = get_access_token(client, "user1", "password123")
    client.post(
        "/send_data",
        json={"data": {"foo": "bar"}},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    response = client.get(
        "/get_data",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
