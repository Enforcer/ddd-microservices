from dataclasses import dataclass

from negotiations.application.availability_port import AvailabilityPort
from negotiations.application.repository import NegotiationsRepository


class AcceptingNegotiation:
    def __init__(
        self, repository: NegotiationsRepository, availability: AvailabilityPort
    ) -> None:
        self._repository = repository
        self._availability = availability

    @dataclass
    class Dto:
        accepting_party_id: int
        buyer_id: int
        seller_id: int
        item_id: int

    def run(self, dto: Dto) -> None:
        negotiation = self._repository.get(
            buyer_id=dto.buyer_id, seller_id=dto.seller_id, item_id=dto.item_id
        )
        negotiation.accept(accepting_party_id=dto.accepting_party_id)
        self._repository.update(negotiation)
        self._availability.reserve(item_id=dto.item_id, buyer_id=dto.buyer_id)
