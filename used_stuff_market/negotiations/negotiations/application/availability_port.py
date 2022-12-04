import abc


class FailedToReserve(Exception):
    pass


class AlreadyReserved(Exception):
    pass


class AvailabilityPort(abc.ABC):
    @abc.abstractmethod
    def reserve(self, item_id: int, buyer_id: int) -> None:
        pass
