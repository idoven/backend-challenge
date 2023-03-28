from datetime import timedelta

import pytest
from fastapi import status

from ecg.api.dependencies.auth import create_access_token
from ecg.domains.admin.models import User
from ecg.domains.ecg.models import LeadTypeEnum


def create_test_token(user: User):
    token = create_access_token(
        {"sub": user.email}, expires_delta=timedelta(minutes=15)
    )
    return token

@pytest.mark.needs_db
def test_add_ecg(test_client, test_user):
    data = {
        "id": "string",
        "date": "2021-01-01T15:20:55.495Z",
        "leads": [
            {
                "name": "I",
                "sample_size": None,
                "signal": [0, 1, 2, 3],
            }
        ],
    }

    token = create_test_token(test_user)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = test_client.post("/api/v1/ecg", headers=headers, json=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "ECG successfully added"}

@pytest.mark.needs_db
def test_get_ecg(test_client, test_user, test_ecg):
    token = create_test_token(test_user)
    response = test_client.get(
        f"/api/v1/ecg/{test_ecg.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": test_ecg.id,
        "leads": [
            {"name": LeadTypeEnum.I, "crossings": 1},
            {"name": LeadTypeEnum.II, "crossings": 2},
        ],
    }

@pytest.mark.needs_db
def test_get_ecg_not_found(test_client, test_user, test_admin, test_ecg):
    token = create_test_token(test_user)
    response = test_client.get(
        "/api/v1/ecg/nonexistent_ecg_id",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = test_client.get(
        f"/api/v1/ecg/{test_ecg.id}",
        headers={"Authorization": f"Bearer {create_test_token(test_admin)}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
