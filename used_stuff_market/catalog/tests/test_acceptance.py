from typing import Iterator
from unittest.mock import Mock

import pytest
import mqlib
from catalog import consumer
from catalog.api import app
from fastapi.testclient import TestClient


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client


def test_item_from_event_is_searchable(client: TestClient) -> None:
    item_id = 10_000
    body = {
        "item_id": item_id,
        "title": "Spam",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "price": {
            "amount": 9.99,
            "currency": "USD",
        },
    }
    consumer.on_item_change(body=body, message=Mock(spec_spet=mqlib.Message))

    term = "consectetur"
    response = client.get(f"/search/{term}")

    assert response.status_code == 200
    assert response.json() == [
        {
            "item_id": item_id,
            "title": "Spam",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "price": {"amount": 9.99, "currency": "USD"},
            "likes": 0,
        }
    ]


def test_item_updates_are_handled(client: TestClient) -> None:
    item_id = 10_001
    body = {
        "item_id": item_id,
        "title": "Ham",
        "description": "Irrelevant description",
        "price": {
            "amount": 19.99,
            "currency": "USD",
        },
    }
    consumer.on_item_change(body=body, message=Mock(spec_spet=mqlib.Message))
    body = {
        "item_id": item_id,
        "title": "Ham",
        "description": "No description anymore",
        "price": {
            "amount": 29.99,
            "currency": "USD",
        },
    }
    consumer.on_item_change(body=body, message=Mock(spec_spet=mqlib.Message))

    term = "anymore"
    response = client.get(f"/search/{term}")

    assert response.status_code == 200
    assert response.json() == [
        {
            "item_id": item_id,
            "title": "Ham",
            "description": "No description anymore",
            "price": {"amount": 29.99, "currency": "USD"},
            "likes": 0,
        }
    ]


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
