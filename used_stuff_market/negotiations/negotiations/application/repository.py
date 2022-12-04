import abc

from negotiations.domain.negotiation import Negotiation


class NegotiationsRepository(abc.ABC):
    class NotFound(Exception):
        pass

    class AlreadyExists(Exception):
        pass

    @abc.abstractmethod
    def insert(self, negotiation: Negotiation) -> None:
        pass

    @abc.abstractmethod
    def update(self, negotiation: Negotiation) -> None:
        pass

    @abc.abstractmethod
    def get(self, item_id: int, buyer_id: int, seller_id: int) -> Negotiation:
        pass
