from uuid import UUID

import httpx
from negotiations.application.availability_port import (
    AlreadyReserved,
    AvailabilityPort,
    FailedToReserve,
)


class AvailabilityClient(AvailabilityPort):
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    def reserve(self, item_id: int, buyer_id: int) -> None:
        locking_party_id = UUID(int=item_id)
        self._lock(locking_party_id=locking_party_id, resource_id=item_id)

    def _lock(self, locking_party_id: UUID, resource_id: int) -> None:
        url = self._base_url + f"/resources/{resource_id}/lock"
        response = httpx.post(url, json={"locking_party": str(locking_party_id)})
        if response.status_code == 403:
            raise AlreadyReserved
        if response.status_code != 204:
            raise FailedToReserve
