from decimal import Decimal
from typing import TypedDict

from items.item import Item
from items.repository import ItemsRepository


class MoneyDto(TypedDict):
    amount: str
    currency: str


class ItemDto(TypedDict):
    id: int
    title: str
    description: str
    starting_price: MoneyDto


class Items:
    def add(
        self,
        owner_id: int,
        title: str,
        description: str,
        starting_price_amount: Decimal,
        starting_price_currency: str,
    ) -> None:
        item = Item(
            owner_id=owner_id,
            title=title,
            description=description,
            starting_price_amount=starting_price_amount,
            starting_price_currency=starting_price_currency,
        )
        repository = ItemsRepository()
        repository.add(item)

    def get_items(self, owner_id: int) -> list[ItemDto]:
        repository = ItemsRepository()
        items = repository.for_owner(owner_id=owner_id)
        return [
            ItemDto(
                id=item.id,
                title=item.title,
                description=item.description,
                starting_price=MoneyDto(
                    amount=self._format_amount(item.starting_price_amount),
                    currency=item.starting_price_currency,
                ),
            )
            for item in items
        ]

    def _format_amount(self, amount: Decimal) -> str:
        decimal_points = 2
        formatter = "{0:." + str(decimal_points) + "f}"
        return formatter.format(amount)
