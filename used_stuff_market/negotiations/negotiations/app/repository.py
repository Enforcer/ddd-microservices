import abc

from negotiations.domain.negotiation import Negotiation


class NotFound(Exception):
    pass


class NegotiationsRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, negotiation: Negotiation) -> None:
        pass

    @abc.abstractmethod
    def pending_for_item(self, item_id: int, buyer_id: int) -> Negotiation:
        pass
