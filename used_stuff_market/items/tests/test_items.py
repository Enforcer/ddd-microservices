from typing import Iterator

import mqlib.testing
import pytest
from fastapi.testclient import TestClient
from items import outbox_processor
from items.api import app
from items.queues import item_cdc


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


@pytest.mark.skip("Not implemented")
def test_message_about_new_item_is_sent(client: TestClient) -> None:
    post_response = client.post(
        "/items",
        json={
            "title": "Lorem Ipsum Dolor Sit Amet",
            "description": "Consectetur adipiscing elit.",
            "price": {
                "amount": 6.99,
                "currency": "USD",
            },
        },
        headers={"user-id": "3"},
    )
    assert post_response.status_code == 204

    # ...?


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


def test_message_about_item_is_sent(client: TestClient) -> None:
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
    outbox_processor.run_once()

    message = mqlib.testing.next_message(item_cdc)
    assert message
