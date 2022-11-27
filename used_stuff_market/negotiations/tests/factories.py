from decimal import Decimal
from typing import Any

import factory
from negotiations.negotiation import Negotiation
from negotiations.repository import NegotiationsRepository


class NegotiationFactory(factory.Factory):
    class Meta:
        model = Negotiation

    item_id = factory.Sequence(lambda n: n + 1)
    seller_id = factory.Sequence(lambda n: n + 1)
    buyer_id = factory.Sequence(lambda n: n + 1)
    price = Decimal("12.99")
    currency = "USD"
    waits_for_decision_of = factory.LazyAttribute(
        lambda negotiation: negotiation.seller_id
    )

    @classmethod
    def create(cls, **kwargs: Any) -> Negotiation:
        instance = super().create(**kwargs)
        repo = NegotiationsRepository()
        repo.insert(instance)
        return instance
