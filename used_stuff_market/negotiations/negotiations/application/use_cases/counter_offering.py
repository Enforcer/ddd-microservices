from dataclasses import dataclass

from negotiations.application.repository import NegotiationsRepository
from negotiations.domain.money import Money


class CounterOfferingNegotiation:
    def __init__(self, repository: NegotiationsRepository) -> None:
        self._repository = repository

    @dataclass
    class Dto:
        counter_offering_party_id: int
        buyer_id: int
        seller_id: int
        item_id: int
        new_price: Money

    def run(self, dto: Dto) -> None:
        negotiation = self._repository.get(
            buyer_id=dto.buyer_id, seller_id=dto.seller_id, item_id=dto.item_id
        )
        negotiation.counteroffer(
            counter_offering_party_id=dto.counter_offering_party_id,
            price=dto.new_price,
        )
        self._repository.update(negotiation)
