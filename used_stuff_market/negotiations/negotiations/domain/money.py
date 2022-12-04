from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, validator


class Currency(StrEnum):
    USD = "USD"


class Money(BaseModel):
    amount: Decimal
    currency: Currency

    @validator("amount")
    def validate_amount(cls, raw_price) -> None:
        if raw_price <= 0:
            raise ValueError("Price must be positive")
        return raw_price
