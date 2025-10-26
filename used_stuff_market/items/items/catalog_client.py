import httpx
import tenacity

from container_or_host import host_for_dependency
from items.item import Item


class BadPayload(Exception):
    pass


class CatalogClient:
    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential() + tenacity.wait_random(0, 2),
        retry=tenacity.retry_if_not_exception_type(BadPayload),
    )
    def register_item(self, item: Item) -> None:
        host = host_for_dependency(addres_for_docker="catalog")
        body = {
            "item_id": item.id,
            "title": item.title,
            "description": item.description,
            "price": {
                "amount": float(item.price_amount),
                "currency": item.price_currency,
            },
        }
        response = httpx.post(f"http://{host}:8400/items", json=body)
        status = response.status_code
        if status >= 400 and status < 500:
            raise BadPayload
        response.raise_for_status()
