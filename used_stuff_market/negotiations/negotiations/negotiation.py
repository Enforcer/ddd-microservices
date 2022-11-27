from decimal import Decimal

from negotiations.money import Money
from pydantic import BaseModel


class Negotiation(BaseModel):
    item_id: int
    seller_id: int
    buyer_id: int
    price: Money
    waits_for_decision_of: int
    broken_off: bool = False
    accepted: bool = False

    class NegotiationConcluded(Exception):
        pass

    class OnlyWaitingSideCanAccept(Exception):
        pass

    class OnlyWaitingSideCanCounteroffer(Exception):
        pass

    def break_off(self) -> None:
        if self.broken_off or self.accepted:
            raise self.NegotiationConcluded
        self.broken_off = True

    def accept(self, user_id: int) -> None:
        if self.broken_off or self.accepted:
            raise self.NegotiationConcluded
        if user_id != self.waits_for_decision_of:
            raise self.OnlyWaitingSideCanAccept
        self.accepted = True

    def counteroffer(self, user_id: int, price: Money) -> None:
        if self.broken_off or self.accepted:
            raise self.NegotiationConcluded

        if user_id != self.waits_for_decision_of:
            raise self.OnlyWaitingSideCanCounteroffer

        if self.waits_for_decision_of == self.seller_id:
            self.waits_for_decision_of = self.buyer_id
        else:
            self.waits_for_decision_of = self.seller_id

        self.price = price
