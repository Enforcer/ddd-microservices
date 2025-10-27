from decimal import Decimal
from typing import TypedDict

import mqlib
from items.item import Item
from items.queues import item_cdc
from items.repository import ItemsRepository


class MoneyDto(TypedDict):
    amount: str
    currency: str


class ItemDto(TypedDict):
    id: int
    title: str
    description: str
    price: MoneyDto


class Items:
    class NoSuchItem(Exception):
        pass

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
            price_amount=starting_price_amount,
            price_currency=starting_price_currency,
        )
        repository = ItemsRepository()
        repository.add(item)
        mqlib.publish(
            item_cdc,
            message={},  # TODO
        )

    def get_items(self, owner_id: int) -> list[ItemDto]:
        repository = ItemsRepository()
        items = repository.for_owner(owner_id=owner_id)
        return [
            ItemDto(
                id=item.id,
                title=item.title,
                description=item.description,
                price=MoneyDto(
                    amount=self._format_amount(item.price_amount),
                    currency=item.price_currency,
                ),
            )
            for item in items
        ]

    def _format_amount(self, amount: Decimal) -> str:
        decimal_points = 2
        formatter = "{0:." + str(decimal_points) + "f}"
        return formatter.format(amount)

    def update(
        self,
        owner_id: int,
        item_id: int,
        title: str,
        description: str,
        price_amount: Decimal,
        price_currency: str,
    ) -> None:
        repository = ItemsRepository()
        try:
            item = repository.get(owner_id=owner_id, item_id=item_id)
        except ItemsRepository.NotFound:
            raise self.NoSuchItem
        else:
            item.title = title
            item.description = description
            item.price_amount = price_amount
            item.price_currency = price_currency

            mqlib.publish(
                item_cdc,
                message={},  # TODO
            )
