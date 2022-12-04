from negotiations.domain import exceptions
from negotiations.domain.money import Money
from pydantic import BaseModel


class Negotiation(BaseModel):
    item_id: int
    seller_id: int
    buyer_id: int
    price: Money
    waits_for_decision_of: int
    broken_off: bool = False
    accepted: bool = False

    def break_off(self, breaking_off_party_id: int) -> None:
        if breaking_off_party_id not in (self.seller_id, self.buyer_id):
            raise exceptions.OnlyParticipantsCanBreakOff
        if self.broken_off or self.accepted:
            raise exceptions.NegotiationConcluded
        self.broken_off = True

    def accept(self, accepting_party_id: int) -> None:
        if self.broken_off or self.accepted:
            raise exceptions.NegotiationConcluded
        if accepting_party_id != self.waits_for_decision_of:
            raise exceptions.OnlyWaitingSideCanAccept
        self.accepted = True

    def counteroffer(self, counter_offering_party_id: int, price: Money) -> None:
        if self.broken_off or self.accepted:
            raise exceptions.NegotiationConcluded

        if counter_offering_party_id != self.waits_for_decision_of:
            raise exceptions.OnlyWaitingSideCanCounteroffer

        if self.waits_for_decision_of == self.seller_id:
            self.waits_for_decision_of = self.buyer_id
        else:
            self.waits_for_decision_of = self.seller_id

        self.price = price
