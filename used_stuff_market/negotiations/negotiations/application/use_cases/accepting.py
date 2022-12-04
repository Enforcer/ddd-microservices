from dataclasses import dataclass
from uuid import UUID

from container_or_host import host_for_dependency
from negotiations.application.repository import NegotiationsRepository
from negotiations.availability_client import AvailabilityClient


class AcceptingNegotiation:
    def __init__(self, repository: NegotiationsRepository) -> None:
        self._repository = repository

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
        availability_host = host_for_dependency(addres_for_docker="availability")
        availability_client = AvailabilityClient(
            base_url=f"http://{availability_host}:8300"
        )
        availability_client.lock(
            locking_party_id=UUID(int=dto.buyer_id), resource_id=dto.item_id
        )
