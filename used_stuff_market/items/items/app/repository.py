import abc

from items.domain.item import Item


class ItemsRepository(abc.ABC):
    class NotFound(Exception):
        pass

    @abc.abstractmethod
    def add(self, item: Item) -> None:
        pass

    @abc.abstractmethod
    def get(self, owner_id: int, item_id: int) -> Item:
        pass

    @abc.abstractmethod
    def for_owner(self, owner_id: int) -> list[Item]:
        pass
