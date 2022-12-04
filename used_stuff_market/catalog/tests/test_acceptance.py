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


@pytest.mark.skip("Not implemented")
def test_item_saved_from_event_is_searchable(client: TestClient) -> None:
    body: dict = {}
    consumer.on_name_me(body=body, message=Mock(spec_spet=mqlib.Message))

    term = "search term"
    response = client.get(f"/search/{term}")

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert response.json() == [...]
