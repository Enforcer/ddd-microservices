import httpx

from container_or_host import host_for_dependency
from items.item import Item


class CatalogClient:
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
        response.raise_for_status()
