from typing import Iterator

import pytest
from catalog.api import app
from fastapi.testclient import TestClient


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client


def test_item_from_api_searchable(client: TestClient) -> None:
    item_id = 1_000
    body = {
        "item_id": item_id,
        "title": "Example",
        "description": "Losowy tekst bez większego znaczenia",
        "price": {
            "amount": 17.99,
            "currency": "USD",
        },
        "version": 1,
    }
    while True:
        register_item_response = client.post(f"/items", json=body)
        if register_item_response.status_code == 200:
            break

    term = "tekst"
    response = client.get(f"/search/{term}")

    assert response.status_code == 200
    assert response.json() == [
        {
            "item_id": item_id,
            "title": "Example",
            "description": "Losowy tekst bez większego znaczenia",
            "price": {"amount": 17.99, "currency": "USD"},
            "likes": 0,
        }
    ]
