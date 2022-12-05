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
    }
    consumer.on_item_added(body=body, message=Mock(spec_spet=mqlib.Message))

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
