from negotiations.domain.money import Money, USD
from negotiations.domain.negotiation import Negotiation, Status

SELLER_ID = 1
BUYER_ID = 2
OPENING_PRICE = Money(USD, "10.99")


def test_seller_can_accept_negotiation_started_by_buyer() -> None:
    negotiation = Negotiation(
        SELLER_ID, BUYER_ID, OPENING_PRICE, started_by_user_id=BUYER_ID
    )

    negotiation.accept(SELLER_ID)

    assert negotiation.status == Status.ACCEPTED


def test_buyer_can_accept_negotiation_started_by_seller() -> None:
    negotiation = Negotiation(
        SELLER_ID, BUYER_ID, OPENING_PRICE, started_by_user_id=BUYER_ID
    )

    negotiation.accept(BUYER_ID)

    assert negotiation.status == Status.ACCEPTED


def test_accepted_negotiation_cannot_be_accepted_again() -> None:
    pass
