from typing import Iterator, Any

import pytest
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock

from items.api import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


class AnyInt(int):
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, int)

    def __repr__(self) -> str:
        return "AnyInt()"


def test_added_item_is_available(client: TestClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response()

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


def test_flakiness_of_catalog_is_handled(
    client: TestClient, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(status_code=500)
    httpx_mock.add_response(status_code=500)
    httpx_mock.add_response(status_code=200)

    post_response = client.post(
        "/items",
        json={
            "title": "Another item",
            "description": "Colorful and costly",
            "price": {
                "amount": 199.99,
                "currency": "USD",
            },
        },
        headers={"user-id": "1"},
    )
    assert post_response.status_code == 204


def test_update_of_item_is_applied(client: TestClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response()

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
    get_response = client.get("/items", headers={"user-id": "2"})
    assert get_response.status_code == 200
    items = get_response.json()
    assert len(items) == 1
    item_id = items[0]["id"]

    post_response = client.put(
        f"/items/{item_id}",
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
            "id": item_id,
            "title": "JOKE THESE WERE JEANS",
            "description": "Plz buy",
            "price": {
                "amount": "9.99",
                "currency": "USD",
            },
        },
    ]
