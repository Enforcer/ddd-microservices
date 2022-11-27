from items.db import ScopedSession, mapper_registry, metadata
from items.item import Item
from sqlalchemy import Column, Integer, Numeric, String, Table


class ItemsRepository:
    def add(self, item: Item) -> None:
        session = ScopedSession()
        session.add(item)
        session.flush()

    def for_owner(self, owner_id: int) -> list[Item]:
        session = ScopedSession()
        items: list[Item] = (
            session.query(Item).filter(Item.owner_id == str(owner_id)).all()
        )
        return items


items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", Integer()),
    Column("title", String()),
    Column("description", String()),
    Column("starting_price_amount", Numeric()),
    Column("starting_price_currency", String(3)),
)


mapper_registry.map_imperatively(
    Item,
    items,
)
