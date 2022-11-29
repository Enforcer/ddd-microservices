from decimal import Decimal

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
    price: Decimal,
    currency: str,
) -> Negotiation:
    if user_id not in (seller_id, buyer_id):
        raise NotABuyerOrSeller

    if price <= 0:
        raise InvalidPrice

    waits_for_decision_of = seller_id if user_id == buyer_id else buyer_id

    return Negotiation(
        item_id=item_id,
        buyer_id=buyer_id,
        seller_id=seller_id,
        price=price,
        currency=currency,
        waits_for_decision_of=waits_for_decision_of,
    )
