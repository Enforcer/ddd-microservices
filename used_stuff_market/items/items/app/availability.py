import abc


class AvailabilityPort(abc.ABC):
    @abc.abstractmethod
    def register_item(self, item_id: int, owner_id: int) -> None:
        pass
