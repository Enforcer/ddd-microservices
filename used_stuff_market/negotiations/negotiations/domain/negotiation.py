import enum

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, composite

from negotiations.domain.money import Money
from negotiations.infrastructure.db import Base


class Status(enum.StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    BROKEN_OFF = "BROKEN_OFF"


class NegotiationEnded(Exception):
    pass


class OnlyOtherUserCanAccept(Exception):
    pass


class NotParticipant(Exception):
    pass


class Negotiation(Base):
    __tablename__ = "negotiations"

    id: Mapped[int] = mapped_column(primary_key=True)
    _item_id: Mapped[int] = mapped_column(name="item_id")
    _seller_id: Mapped[int] = mapped_column(name="seller_id")
    _buyer_id: Mapped[int] = mapped_column(name="buyer_id")
    _proposed_price: Mapped[Money] = composite(
        mapped_column("total_currency", String(3)),
        mapped_column("total_amount", Numeric()),
    )
    _started_by_user_id: Mapped[int] = mapped_column(name="started_by_user_id")
    _status: Mapped[Status] = mapped_column(name="status")

    def __init__(
        self,
        item_id: int,
        seller_id: int,
        buyer_id: int,
        proposed_price: Money,
        started_by_user_id: int,
    ) -> None:
        self._item_id = item_id
        self._seller_id = seller_id
        self._buyer_id = buyer_id
        self._proposed_price = proposed_price
        self._started_by_user_id = started_by_user_id
        self._status = Status.PENDING

    @property
    def status(self) -> Status:
        return self._status

    def accept(self, user_id: int) -> None:
        self._ensure_pending()
        self._ensure_participant(user_id)
        if self._started_by_user_id == user_id:
            raise OnlyOtherUserCanAccept

        self._status = Status.ACCEPTED

    def break_off(self, user_id: int) -> None:
        self._ensure_pending()
        self._ensure_participant(user_id)
        self._status = Status.BROKEN_OFF

    def _ensure_pending(self) -> None:
        if self._status != Status.PENDING:
            raise NegotiationEnded

    def _ensure_participant(self, user_id: int) -> None:
        if user_id not in (self._buyer_id, self._seller_id):
            raise NotParticipant
