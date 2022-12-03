from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from items.api import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def test_added_item_is_available(client: TestClient) -> None:
    post_response = client.post(
        "/items",
        json={
            "title": "Cool socks",
            "description": "A very nice item",
            "price": {
                "amount": 10.99,
                "currency": "USD",
            },
        },
        headers={"user-id": "1"},
    )
    assert post_response.status_code == 204

    get_response = client.get("/items", headers={"user-id": "1"})
    assert get_response.status_code == 200
    assert get_response.json() == [
        {
            "id": 1,
            "title": "Cool socks",
            "description": "A very nice item",
            "price": {
                "amount": "10.99",
                "currency": "USD",
            },
        },
    ]


def test_update_of_item_is_applied(client: TestClient) -> None:
    post_response = client.post(
        "/items",
        json={
            "title": "Really nice pants",
            "description": "Pink pants, a vivid colour!",
            "price": {
                "amount": 19.99,
                "currency": "USD",
            },
        },
        headers={"user-id": "2"},
    )
    assert post_response.status_code == 204

    post_response = client.put(
        "/items/2",
        json={
            "title": "JOKE THESE WERE JEANS",
            "description": "Plz buy",
            "price": {
                "amount": 9.99,
                "currency": "USD",
            },
        },
        headers={"user-id": "2"},
    )
    assert post_response.status_code == 204

    get_response = client.get("/items", headers={"user-id": "2"})
    assert get_response.status_code == 200
    assert get_response.json() == [
        {
            "id": 2,
            "title": "JOKE THESE WERE JEANS",
            "description": "Plz buy",
            "price": {
                "amount": "9.99",
                "currency": "USD",
            },
        },
    ]
