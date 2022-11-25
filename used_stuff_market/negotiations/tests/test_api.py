from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from negotiations.api import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.skip("Not implemented")
def test_broken_off_negotiation_is_no_longer_returned(client: TestClient) -> None:
    buyer_id = 1
    seller_id = 2
    item_id = 123
    create_response = client.post(
        f"/items/{item_id}/negotiations",
        json={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "price": "1.99",
            "currency": "USD",
        },
        headers={"user-id": str(seller_id)},
    )
    assert create_response.status_code == 204, create_response.json()

    break_off_response = client.delete(
        f"/items/{item_id}/negotiations",
        params={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
        },
        headers={"user-id": str(seller_id)},
    )
    assert break_off_response.status_code == 204, break_off_response.json()

    get_response = client.get(
        f"/items/{item_id}/negotiations",
        params={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
        },
        headers={"user-id": str(seller_id)},
    )
    assert get_response.status_code == 404, get_response.json()
