import functools
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, validator


class Currency(StrEnum):
    USD = "USD"


@functools.total_ordering
class Money(BaseModel):
    amount: Decimal
    currency: Currency

    @validator("amount")
    def validate_amount(cls, raw_price) -> None:
        if raw_price <= 0:
            raise ValueError("Price must be positive")
        return raw_price

    def __sub__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            raise TypeError("Can only subtract Money from Money")
        if self.currency != other.currency:
            raise TypeError("Can only subtract same currency Money")
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def __lt__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            raise TypeError("Can only compare Money with Money")
        if self.currency != other.currency:
            raise TypeError("Can only compare Money with same currency")
        return self.amount < other.amount
