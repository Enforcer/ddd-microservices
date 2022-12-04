from dataclasses import dataclass

from negotiations.negotiation import Negotiation
from negotiations.repository import NegotiationsRepository


class GettingNegotiation:
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

        repository = NegotiationsRepository()
        negotiation = repository.get(
            buyer_id=dto.buyer_id,
            seller_id=dto.seller_id,
            item_id=dto.item_id,
        )
        if negotiation.broken_off:
            raise self.NegotiationNoLongerAvailable

        return negotiation
