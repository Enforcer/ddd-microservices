from dataclasses import dataclass

from negotiations.application.repository import NegotiationsRepository


class BreakingOffNegotiation:
    def __init__(self, repository: NegotiationsRepository) -> None:
        self._repository = repository

    @dataclass
    class Dto:
        breaking_off_party_id: int
        buyer_id: int
        seller_id: int
        item_id: int

    def run(self, dto: Dto) -> None:
        negotiation = self._repository.get(
            buyer_id=dto.buyer_id, seller_id=dto.seller_id, item_id=dto.item_id
        )
        negotiation.break_off(breaking_off_party_id=dto.breaking_off_party_id)
        self._repository.update(negotiation=negotiation)
