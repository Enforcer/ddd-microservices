from dataclasses import dataclass

from negotiations import factory
from negotiations.money import Money
from negotiations.repository import NegotiationsRepository


class StartingNegotiation:
    @dataclass
    class Dto:
        accepting_party_id: int
        item_id: int
        seller_id: int
        buyer_id: int
        starting_price: Money

    def run(self, dto: Dto) -> None:
        repository = NegotiationsRepository()
        negotiation = factory.build_negotiation(
            user_id=dto.accepting_party_id,
            item_id=dto.item_id,
            seller_id=dto.seller_id,
            buyer_id=dto.buyer_id,
            price=dto.starting_price,
        )
        repository.insert(negotiation)
