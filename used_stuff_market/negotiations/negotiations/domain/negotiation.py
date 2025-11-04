import enum

from negotiations.domain.money import Money


class Status(enum.StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    BROKEN_OFF = "BROKEN_OFF"


class Negotiation:
    def __init__(
        self,
        seller_id: int,
        buyer_id: int,
        proposed_price: Money,
        started_by_user_id: int,
    ) -> None:
        self._seller_id = seller_id
        self._buyer_id = buyer_id
        self._proposed_price = proposed_price
        self._started_by_user_id = started_by_user_id
        self._status = Status.PENDING

    @property
    def status(self) -> Status:
        return self._status

    def accept(self, user_id: int) -> None:
        pass

    def break_off(self, user_id: int) -> None:
        pass
