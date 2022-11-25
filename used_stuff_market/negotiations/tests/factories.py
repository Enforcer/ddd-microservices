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

    @classmethod
    def create(cls, **kwargs: Any) -> Negotiation:
        instance = super().create(**kwargs)
        repo = NegotiationsRepository()
        repo.save(instance)
        return instance
