import pytest

from negotiations.domain.money import Money, USD
from negotiations.domain.negotiation import Negotiation, Status, NegotiationEnded

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
        SELLER_ID, BUYER_ID, OPENING_PRICE, started_by_user_id=SELLER_ID
    )

    negotiation.accept(BUYER_ID)

    assert negotiation.status == Status.ACCEPTED


def test_accepted_negotiation_cannot_be_accepted_again() -> None:
    negotiation = Negotiation(
        SELLER_ID, BUYER_ID, OPENING_PRICE, started_by_user_id=SELLER_ID
    )

    negotiation.accept(BUYER_ID)

    with pytest.raises(NegotiationEnded):
        negotiation.accept(BUYER_ID)


@pytest.mark.parametrize("started_by_user_id", [SELLER_ID, BUYER_ID])
@pytest.mark.parametrize("side_breaking_off", [SELLER_ID, BUYER_ID])
def test_broken_off_negotiation_cannot_be_broken_off_again(
    started_by_user_id: int, side_breaking_off: int
) -> None:
    negotiation = Negotiation(
        SELLER_ID, BUYER_ID, OPENING_PRICE, started_by_user_id=started_by_user_id
    )

    negotiation.break_off(side_breaking_off)

    with pytest.raises(NegotiationEnded):
        negotiation.break_off(side_breaking_off)
