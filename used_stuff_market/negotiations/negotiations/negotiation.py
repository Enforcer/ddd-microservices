from decimal import Decimal

from pydantic import BaseModel


class Negotiation(BaseModel):
    item_id: int
    seller_id: int
    buyer_id: int
    price: Decimal
    currency: str
    broken_off: bool = False
    accepted: bool = False

    class NegotiationConcluded(Exception):
        pass

    class OnlySellerCanAccept(Exception):
        pass

    def break_off(self) -> None:
        if self.broken_off or self.accepted:
            raise self.NegotiationConcluded
        self.broken_off = True

    def accept(self, user_id: int) -> None:
        if self.broken_off or self.accepted:
            raise self.NegotiationConcluded
        if user_id != self.seller_id:
            raise self.OnlySellerCanAccept
        self.accepted = True
