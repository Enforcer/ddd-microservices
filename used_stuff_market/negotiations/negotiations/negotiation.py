from negotiations.money import Money
from pydantic import BaseModel, Field


class Negotiation(BaseModel):
    item_id: int
    seller_id: int
    buyer_id: int
    price: Money
    waits_for_decision_of: int
    broken_off: bool = False
    accepted: bool = False
    canceled: bool = False
    version: int = 1

    class NegotiationConcluded(Exception):
        pass

    class OnlyWaitingSideCanAccept(Exception):
        pass

    class OnlyWaitingSideCanCounteroffer(Exception):
        pass

    def break_off(self) -> None:
        self._ensure_negotiation_pending()
        self.broken_off = True

    def accept(self, user_id: int) -> None:
        self._ensure_negotiation_pending()
        if user_id != self.waits_for_decision_of:
            raise self.OnlyWaitingSideCanAccept
        self.accepted = True

    def cancel(self) -> None:
        self._ensure_negotiation_pending()
        self.canceled = True

    def _ensure_negotiation_pending(self) -> None:
        if self.broken_off or self.accepted or self.canceled:
            raise self.NegotiationConcluded

    def counteroffer(self, user_id: int, price: Money) -> None:
        self._ensure_negotiation_pending()

        if user_id != self.waits_for_decision_of:
            raise self.OnlyWaitingSideCanCounteroffer

        if self.waits_for_decision_of == self.seller_id:
            self.waits_for_decision_of = self.buyer_id
        else:
            self.waits_for_decision_of = self.seller_id

        self.price = price
