from typing import Iterator
from unittest.mock import Mock

import mqlib
import pytest
from catalog import consumer
from catalog.api import app
from fastapi.testclient import TestClient


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client


def test_item_from_event_is_searchable(client: TestClient) -> None:
    body = {
        "item_id": 10_000,
        "title": "Spam",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "price": {
            "amount": 9.99,
            "currency": "USD",
        },
        "version": 1,
    }
    consumer.on_item_change(body=body, message=Mock(spec_spet=mqlib.Message))

    term = "consectetur"
    response = client.get(f"/search/{term}")

    assert response.status_code == 200
    assert response.json() == [
        {
            "item_id": 10000,
            "title": "Spam",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "price": {"amount": 9.99, "currency": "USD"},
        }
    ]


def test_another_message_with_same_version_is_ignored(client: TestClient) -> None:
    body = {
        "item_id": 20_000,
        "title": "Another message",
        "description": "Another description.",
        "price": {
            "amount": 1.99,
            "currency": "USD",
        },
        "version": 1,
    }
    consumer.on_item_change(body=body, message=Mock(spec_spet=mqlib.Message))
    another_message = body.copy()
    another_message["title"] = "Oupsie!"
    consumer.on_item_change(body=body, message=Mock(spec_spet=mqlib.Message))

    term = "description"
    response = client.get(f"/search/{term}")

    assert response.status_code == 200
    assert response.json() == [
        {
            "item_id": 20_000,
            "title": "Another message",
            "description": "Another description.",
            "price": {
                "amount": 1.99,
                "currency": "USD",
            },
        }
    ]
