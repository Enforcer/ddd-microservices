from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from negotiations.api import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


user_ids = iter(range(1, 10_000))
item_ids = iter(range(1, 10_000))


def test_started_negotiation_is_returned(client: TestClient) -> None:
    buyer_id = next(user_ids)
    seller_id = next(user_ids)
    item_id = next(item_ids)
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

    get_response = client.get(
        f"/items/{item_id}/negotiations",
        params={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
        },
        headers={"user-id": str(seller_id)},
    )
    assert get_response.status_code == 200
    assert get_response.json() == {
        "item_id": item_id,
        "seller_id": seller_id,
        "buyer_id": buyer_id,
        "price": 1.99,
        "currency": "USD",
        "broken_off": False,
        "accepted": False,
        "waits_for_decision_of": buyer_id,
    }


def test_broken_off_negotiation_is_no_longer_returned(client: TestClient) -> None:
    buyer_id = next(user_ids)
    seller_id = next(user_ids)
    item_id = next(item_ids)
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


def test_cant_accept_same_negotiation_twice(client: TestClient) -> None:
    buyer_id = next(user_ids)
    seller_id = next(user_ids)
    item_id = next(item_ids)

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

    accept_response = client.post(
        f"/items/{item_id}/negotiations/accept",
        params={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
        },
        headers={"user-id": str(buyer_id)},
    )
    assert accept_response.status_code == 204, accept_response.json()

    another_accept_response = client.post(
        f"/items/{item_id}/negotiations/accept",
        params={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
        },
        headers={"user-id": str(buyer_id)},
    )
    assert another_accept_response.status_code == 422, accept_response.text


def test_only_seller_can_accept_negotiations(client: TestClient) -> None:
    buyer_id = next(user_ids)
    seller_id = next(user_ids)
    item_id = next(item_ids)

    create_response = client.post(
        f"/items/{item_id}/negotiations",
        json={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "price": "1.99",
            "currency": "USD",
        },
        headers={"user-id": str(buyer_id)},
    )
    assert create_response.status_code == 204, create_response.json()

    accept_response = client.post(
        f"/items/{item_id}/negotiations/accept",
        params={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
        },
        headers={"user-id": str(buyer_id)},
    )
    assert accept_response.status_code == 403, accept_response.json()


def test_cant_break_off_same_negotiation_twice(client: TestClient) -> None:
    buyer_id = next(user_ids)
    seller_id = next(user_ids)
    item_id = next(item_ids)
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

    another_break_off_response = client.delete(
        f"/items/{item_id}/negotiations",
        params={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
        },
        headers={"user-id": str(seller_id)},
    )
    assert another_break_off_response.status_code == 422


def test_buyer_can_accept_after_counteroffer(client: TestClient) -> None:
    buyer_id = next(user_ids)
    seller_id = next(user_ids)
    item_id = next(item_ids)

    create_response = client.post(
        f"/items/{item_id}/negotiations",
        json={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "price": "1.99",
            "currency": "USD",
        },
        headers={"user-id": str(buyer_id)},
    )
    assert create_response.status_code == 204, create_response.json()

    counteroffer_response = client.post(
        f"/items/{item_id}/negotiations/counteroffer",
        json={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "price": "1.99",
            "currency": "USD",
        },
        headers={"user-id": str(seller_id)},
    )
    assert counteroffer_response.status_code == 204, create_response.text

    accept_response = client.post(
        f"/items/{item_id}/negotiations/accept",
        params={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
        },
        headers={"user-id": str(buyer_id)},
    )
    assert accept_response.status_code == 204, accept_response.json()


def test_seller_cannot_accept_after_theirs_counteroffer(client: TestClient) -> None:
    buyer_id = next(user_ids)
    seller_id = next(user_ids)
    item_id = next(item_ids)

    create_response = client.post(
        f"/items/{item_id}/negotiations",
        json={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "price": "1.99",
            "currency": "USD",
        },
        headers={"user-id": str(buyer_id)},
    )
    assert create_response.status_code == 204, create_response.json()

    counteroffer_response = client.post(
        f"/items/{item_id}/negotiations/counteroffer",
        json={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "price": "1.99",
            "currency": "USD",
        },
        headers={"user-id": str(seller_id)},
    )
    assert counteroffer_response.status_code == 204, create_response.text

    accept_response = client.post(
        f"/items/{item_id}/negotiations/accept",
        params={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
        },
        headers={"user-id": str(seller_id)},
    )
    assert accept_response.status_code == 403, accept_response.json()


def test_buyer_can_accept_after_counteroffer_from_them_and_then_buyer(
    client: TestClient,
) -> None:
    buyer_id = next(user_ids)
    seller_id = next(user_ids)
    item_id = next(item_ids)

    create_response = client.post(
        f"/items/{item_id}/negotiations",
        json={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "price": "1.99",
            "currency": "USD",
        },
        headers={"user-id": str(buyer_id)},
    )
    assert create_response.status_code == 204, create_response.json()

    counteroffer_response = client.post(
        f"/items/{item_id}/negotiations/counteroffer",
        json={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "price": "1.99",
            "currency": "USD",
        },
        headers={"user-id": str(seller_id)},
    )
    assert counteroffer_response.status_code == 204, create_response.text

    another_counteroffer_response = client.post(
        f"/items/{item_id}/negotiations/counteroffer",
        json={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "price": "1.99",
            "currency": "USD",
        },
        headers={"user-id": str(buyer_id)},
    )
    assert another_counteroffer_response.status_code == 204, create_response.text

    accept_response = client.post(
        f"/items/{item_id}/negotiations/accept",
        params={
            "seller_id": seller_id,
            "buyer_id": buyer_id,
        },
        headers={"user-id": str(seller_id)},
    )
    assert accept_response.status_code == 204, accept_response.json()
