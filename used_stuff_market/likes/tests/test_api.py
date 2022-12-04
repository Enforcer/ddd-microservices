from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from likes.api import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client


def test_like_can_be_given_and_taken_away(client: TestClient) -> None:
    item_id = 1
    response = client.get(f"/items/{item_id}/likes")
    assert response.status_code == 200
    assert response.json() == {"likes": 0}

    user_id = 2
    response = client.post(f"/items/{item_id}/likes", headers={"user-id": str(user_id)})
    assert response.status_code == 201

    response = client.get(f"/items/{item_id}/likes")
    assert response.status_code == 200
    assert response.json() == {"likes": 1}

    response = client.delete(
        f"/items/{item_id}/likes", headers={"user-id": str(user_id)}
    )
    assert response.status_code == 204

    response = client.get(f"/items/{item_id}/likes")
    assert response.status_code == 200
    assert response.json() == {"likes": 0}
