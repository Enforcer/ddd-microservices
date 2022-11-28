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


class NegotiationsFeature:
    class NotFound(Exception):
        pass

    class CantAccept(Exception):
        pass

    class CantBreakOff(Exception):
        pass

    def __init__(self, client: TestClient) -> None:
        self._client = client
        self.seller_id = next(user_ids)
        self.buyer_id = next(item_ids)
        self.item_id = next(item_ids)

    def start(
        self, who: int | None = None, price: str = "1.99", currency: str = "USD"
    ) -> None:
        if who is None:
            who = self.buyer_id

        create_response = self._client.post(
            f"/items/{self.item_id}/negotiations",
            json={
                "seller_id": self.seller_id,
                "buyer_id": self.buyer_id,
                "price": price,
                "currency": currency,
            },
            headers={"user-id": str(who)},
        )
        assert create_response.status_code == 204, create_response.json()

    def get(self) -> dict:
        get_response = self._client.get(
            f"/items/{self.item_id}/negotiations",
            params={
                "seller_id": self.seller_id,
                "buyer_id": self.buyer_id,
            },
            headers={"user-id": str(self.seller_id)},
        )
        if get_response.status_code == 404:
            raise self.NotFound

        assert get_response.status_code == 200
        return get_response.json()

    def break_off(self) -> None:
        break_off_response = self._client.delete(
            f"/items/{self.item_id}/negotiations",
            params={
                "seller_id": self.seller_id,
                "buyer_id": self.buyer_id,
            },
            headers={"user-id": str(self.seller_id)},
        )
        if break_off_response.status_code == 422:
            raise self.CantBreakOff

        assert break_off_response.status_code == 204, break_off_response.json()

    def accept(self, who: int | None = None) -> None:
        if who is None:
            who = self.seller_id

        accept_response = self._client.post(
            f"/items/{self.item_id}/negotiations/accept",
            params={
                "seller_id": self.seller_id,
                "buyer_id": self.buyer_id,
            },
            headers={"user-id": str(who)},
        )
        if accept_response.status_code in (422, 403):
            raise self.CantAccept

        assert accept_response.status_code == 204, accept_response.json()

    def counteroffer(self, who: int | None = None) -> None:
        if who is None:
            who = self.seller_id

        counteroffer_response = self._client.post(
            f"/items/{self.item_id}/negotiations/counteroffer",
            json={
                "seller_id": self.seller_id,
                "buyer_id": self.buyer_id,
                "price": "1.99",
                "currency": "USD",
            },
            headers={"user-id": str(who)},
        )
        assert counteroffer_response.status_code == 204, counteroffer_response.text


@pytest.fixture()
def feature_object(client: TestClient) -> NegotiationsFeature:
    return NegotiationsFeature(client=client)


def test_started_negotiation_is_returned(feature_object: NegotiationsFeature) -> None:
    feature_object.start()

    negotiation = feature_object.get()
    assert negotiation == {
        "item_id": feature_object.item_id,
        "seller_id": feature_object.seller_id,
        "buyer_id": feature_object.buyer_id,
        "price": 1.99,
        "currency": "USD",
        "broken_off": False,
        "accepted": False,
        "waits_for_decision_of": feature_object.seller_id,
    }


def test_broken_off_negotiation_is_no_longer_returned(
    feature_object: NegotiationsFeature,
) -> None:
    feature_object.start()

    feature_object.break_off()

    with pytest.raises(NegotiationsFeature.NotFound):
        feature_object.get()


def test_cant_accept_same_negotiation_twice(
    feature_object: NegotiationsFeature,
) -> None:
    feature_object.start()

    feature_object.accept()

    with pytest.raises(NegotiationsFeature.CantAccept):
        feature_object.accept()


def test_only_seller_can_accept_negotiations(
    feature_object: NegotiationsFeature,
) -> None:
    feature_object.start(who=feature_object.buyer_id)

    with pytest.raises(NegotiationsFeature.CantAccept):
        feature_object.accept(who=feature_object.buyer_id)


def test_cant_break_off_same_negotiation_twice(
    feature_object: NegotiationsFeature,
) -> None:
    feature_object.start()
    feature_object.break_off()

    with pytest.raises(NegotiationsFeature.CantBreakOff):
        feature_object.break_off()


def test_buyer_can_accept_after_counteroffer(
    feature_object: NegotiationsFeature,
) -> None:
    feature_object.start()
    feature_object.counteroffer(who=feature_object.seller_id)

    feature_object.accept(who=feature_object.buyer_id)

    assert feature_object.get()["accepted"] is True


def test_seller_cannot_accept_after_theirs_counteroffer(
    feature_object: NegotiationsFeature,
) -> None:
    feature_object.start()
    feature_object.counteroffer(who=feature_object.seller_id)

    with pytest.raises(NegotiationsFeature.CantAccept):
        feature_object.accept(who=feature_object.seller_id)


def test_seller_can_accept_after_counteroffer_from_them_and_then_buyer(
    feature_object: NegotiationsFeature,
) -> None:
    feature_object.start()
    feature_object.counteroffer(who=feature_object.seller_id)
    feature_object.counteroffer(who=feature_object.buyer_id)

    feature_object.accept(who=feature_object.seller_id)

    assert feature_object.get()["accepted"] is True
