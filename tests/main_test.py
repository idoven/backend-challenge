import datetime
from fastapi.testclient import TestClient

from main import app
from config.config import database
from models.ecg_models import ECGResults
from utilities.record import Record

client = TestClient(app)
tokens_collection = dict()  # Hashing is slow, so we avoid it as much as possible by caching tokens


def helper_get_valid_token(username: str) -> str:
    password = "password"
    if username not in tokens_collection:
        token_response = client.post("user/token",
                                     headers={"Content-Type": "application/x-www-form-urlencoded"},
                                     data={"username": username, "password": password})
        tokens_collection[username] = token_response.json()["access_token"]
    return tokens_collection[username]


def helper_insert_record(record_id=100, username="user1"):
    result = ECGResults(id=record_id, date=datetime.datetime.now(), lead_results=[])
    database.add_record(record_id, Record(result, username))


def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome, for documentation go to /docs"}


def test_get_token_not_existing_user():
    username = "other"
    password = "password"
    response = client.post("user/token",
                           headers={"Content-Type": "application/x-www-form-urlencoded"},
                           data={"username": username, "password": password})
    assert response.status_code == 401


def test_get_token_wrong_password():
    username = "user1"
    password = "other"
    response = client.post("user/token",
                           headers={"Content-Type": "application/x-www-form-urlencoded"},
                           data={"username": username, "password": password})
    assert response.status_code == 401


def test_get_token_correct_credentials():
    username = "user1"
    password = "password"
    response = client.post("user/token",
                           headers={"Content-Type": "application/x-www-form-urlencoded"},
                           data={"username": username, "password": password})
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"


def test_get_current_user_no_authentication():
    response = client.get("/user/me")
    assert response.status_code == 401


def test_get_current_user_authenticated():
    response = client.get("/user/me",
                          headers={"Authorization": f"Bearer {helper_get_valid_token('user1')}"})
    assert response.status_code == 200
    assert response.json()["username"] == "user1"


def test_retrieve_results_unauthenticated():
    response = client.get("/ecg/get/100")
    assert response.status_code == 401


def test_retrieve_results_authenticated_bad_format():
    response = client.get("/ecg/get/abc",
                          headers={"Authorization": f"Bearer {helper_get_valid_token('user1')}"})
    assert response.status_code == 422


def test_retrieve_results_authenticated_non_existing_record():
    response = client.get("/ecg/get/100",
                          headers={"Authorization": f"Bearer {helper_get_valid_token('user1')}"})
    assert response.status_code == 422


def test_retrieve_results_authenticated_as_admin():
    helper_insert_record(record_id=100, username="admin")
    response = client.get("/ecg/get/100",
                          headers={"Authorization": f"Bearer {helper_get_valid_token('admin')}"})
    assert response.status_code == 401


def test_retrieve_results_authenticated_not_owner_of_record():
    helper_insert_record(record_id=100, username="user2")
    response = client.get("/ecg/get/100",
                          headers={"Authorization": f"Bearer {helper_get_valid_token('user1')}"})
    assert response.status_code == 401


def test_retrieve_results_authenticated_correct_record():
    helper_insert_record(record_id=100, username="user1")
    response = client.get("/ecg/get/100",
                          headers={"Authorization": f"Bearer {helper_get_valid_token('user1')}"})
    assert response.status_code == 200
    assert response.json()["result"]["id"] == 100


def test_ingest_unauthenticated():
    response = client.post("/ecg/submit")
    assert response.status_code == 401


def test_ingest_authenticated_invalid_data():
    response = client.post("/ecg/submit",
                           headers={"Authorization": f"Bearer {helper_get_valid_token('user1')}"})
    assert response.status_code == 422


def test_ingest_authenticated_valid_data():
    response = client.post("/ecg/submit",
                           headers={"Authorization": f"Bearer {helper_get_valid_token('user1')}"},
                           json={"id": 234,
                                 "date": "2023-05-31 17:59:00",
                                 "leads": [{"name": "l", "signal": []}]
                                 })
    assert response.status_code == 200


def test_ingest_authenticated_as_admin():
    response = client.post("/ecg/submit",
                           headers={"Authorization": f"Bearer {helper_get_valid_token('admin')}"},
                           json={"id": 234,
                                 "date": "2023-05-31 17:59:00",
                                 "leads": [{"name": "l", "signal": []}]
                                 })
    assert response.status_code == 401


def test_register_user_unauthenticated():
    response = client.post("/user/register",
                           json={
                               "username": "user3",
                               "password": "password"
                           })
    assert response.status_code == 401


def test_register_user_not_admin():
    response = client.post("/user/register",
                           headers={"Authorization": f"Bearer {helper_get_valid_token('user1')}"},
                           json={
                               "username": "user3",
                               "password": "password"
                           })
    assert response.status_code == 401


def test_register_user_as_admin_repeated_username():
    response = client.post("/user/register",
                           headers={"Authorization": f"Bearer {helper_get_valid_token('admin')}"},
                           json={
                               "username": "user1",
                               "password": "password"
                           })
    assert response.status_code == 422


def test_register_user_as_admin_valid_username():
    response = client.post("/user/register",
                           headers={"Authorization": f"Bearer {helper_get_valid_token('admin')}"},
                           json={
                               "username": "user4",
                               "password": "password"
                           })
    assert response.status_code == 200
