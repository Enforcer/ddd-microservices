from dataclasses import dataclass

from negotiations.repository import NegotiationsRepository


class AcceptingNegotiation:
    @dataclass
    class Dto:
        accepting_party_id: int
        buyer_id: int
        seller_id: int
        item_id: int

    def run(self, dto: Dto) -> None:
        repository = NegotiationsRepository()
        negotiation = repository.get(
            buyer_id=dto.buyer_id, seller_id=dto.seller_id, item_id=dto.item_id
        )
        negotiation.accept(accepting_party_id=dto.accepting_party_id)
        repository.update(negotiation)
