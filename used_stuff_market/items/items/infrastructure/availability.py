from uuid import UUID

import httpx

from items.app.availability import AvailabilityPort


class AvailabilityHttpClient(AvailabilityPort):
    def __init__(self, base_url: str) -> None:
        self._client = httpx.Client(base_url=base_url)

    def register_item(self, item_id: int, owner_id: int) -> None:
        response = self._client.post("/resources", json={
            "resource_id": item_id,
            "owner_id": str(UUID(int=owner_id)),
        })
        response.raise_for_status()
