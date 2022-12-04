from dataclasses import dataclass

from negotiations.application.repository import NegotiationsRepository
from negotiations.domain.negotiation import Negotiation


class GettingNegotiation:
    def __init__(self, repository: NegotiationsRepository) -> None:
        self._repository = repository

    @dataclass
    class Dto:
        requesting_party_id: int
        seller_id: int
        buyer_id: int
        item_id: int

    class NegotiationNoLongerAvailable(Exception):
        pass

    class RequestedByNonParticipant(Exception):
        pass

    def run(self, dto: Dto) -> Negotiation:
        if dto.requesting_party_id not in (dto.seller_id, dto.buyer_id):
            raise self.RequestedByNonParticipant

        negotiation = self._repository.get(
            buyer_id=dto.buyer_id,
            seller_id=dto.seller_id,
            item_id=dto.item_id,
        )
        if negotiation.broken_off:
            raise self.NegotiationNoLongerAvailable

        return negotiation
