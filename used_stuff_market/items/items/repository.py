from items.db import ScopedSession, mapper_registry, metadata
from items.item import Item
from sqlalchemy import Column, Integer, Numeric, String, Table
from sqlalchemy.exc import NoResultFound


class ItemsRepository:
    class NotFound(Exception):
        pass

    def add(self, item: Item) -> None:
        session = ScopedSession()
        session.add(item)
        session.flush()

    def get(self, owner_id: int, item_id: int) -> Item:
        session = ScopedSession()
        try:
            return (
                session.query(Item)
                .filter(Item.owner_id == owner_id, Item.id == item_id)
                .one()
            )
        except NoResultFound:
            raise self.NotFound

    def for_owner(self, owner_id: int) -> list[Item]:
        session = ScopedSession()
        items: list[Item] = session.query(Item).filter(Item.owner_id == owner_id).all()
        return items


items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", Integer(), nullable=False),
    Column("title", String(), nullable=False),
    Column("description", String(), nullable=False),
    Column("price_amount", Numeric(), nullable=False),
    Column("price_currency", String(3), nullable=False),
    Column("version_id", Integer(), nullable=False),
)


mapper_registry.map_imperatively(
    Item,
    items,
    version_id_col=items.c.version_id,
)
