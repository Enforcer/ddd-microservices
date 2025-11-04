from negotiations.domain.money import Money, USD
from negotiations.domain.negotiation import Negotiation
from negotiations.infrastructure.db import session_factory
from negotiations.infrastructure.repository import SqlAlchemyNegotiationsRepository


def test_added_negotiation_can_be_found() -> None:
    repository = SqlAlchemyNegotiationsRepository(session_factory())
    negotiation = Negotiation(
        item_id=1,
        seller_id=2,
        buyer_id=3,
        proposed_price=Money(USD, 10),
        started_by_user_id=3,
    )

    repository.add(negotiation)

    result = repository.pending_for_item(item_id=1, buyer_id=3)

    assert isinstance(result, Negotiation)
