from decimal import Decimal

from negotiations.money import Money
from negotiations.negotiation import Negotiation


class NotABuyerOrSeller(Exception):
    pass


class InvalidPrice(ValueError):
    pass


def build_negotiation(
    user_id: int,
    item_id: int,
    seller_id: int,
    buyer_id: int,
    price: Money,
) -> Negotiation:
    if user_id not in (seller_id, buyer_id):
        raise NotABuyerOrSeller

    return Negotiation(
        item_id=item_id,
        buyer_id=buyer_id,
        seller_id=seller_id,
        price=price,
        waits_for_decision_of=seller_id,
    )
