from dataclasses import dataclass

from negotiations.application.repository import NegotiationsRepository
from negotiations.domain import factory
from negotiations.domain.money import Money


class StartingNegotiation:
    def __init__(self, repository: NegotiationsRepository) -> None:
        self._repository = repository

    @dataclass
    class Dto:
        accepting_party_id: int
        item_id: int
        seller_id: int
        buyer_id: int
        starting_price: Money

    def run(self, dto: Dto) -> None:
        negotiation = factory.build_negotiation(
            user_id=dto.accepting_party_id,
            item_id=dto.item_id,
            seller_id=dto.seller_id,
            buyer_id=dto.buyer_id,
            price=dto.starting_price,
        )
        self._repository.insert(negotiation)
