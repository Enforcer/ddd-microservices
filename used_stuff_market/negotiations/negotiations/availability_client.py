from uuid import UUID

import httpx


class FailedToLockResource(Exception):
    pass


class AlreadyLocked(Exception):
    pass


class AvailabilityClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    def lock(self, locking_party_id: UUID, resource_id: int) -> None:
        url = self._base_url + f"/resources/{resource_id}/lock"
        response = httpx.post(url, json={"locking_party": str(locking_party_id)})
        if response.status_code == 403:
            raise AlreadyLocked
        if response.status_code != 204:
            raise FailedToLockResource
