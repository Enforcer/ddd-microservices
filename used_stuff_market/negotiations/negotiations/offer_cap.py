from decimal import Decimal
from typing import Protocol

from negotiations.money import Currency, Money


class Strategy(Protocol):
    def __call__(self, old_price: Money, new_price: Money) -> None:
        pass


def no_limits(old_price: Money, new_price: Money) -> None:
    pass


def no_more_than_5_usd(old_price: Money, new_price: Money) -> None:
    if old_price - new_price > Money(amount=5, currency=Currency.USD):
        raise ValueError("Can't counteroffer more than 5 USD")


def no_more_than_10_percent(old_price: Money, new_price: Money) -> None:
    difference = old_price - new_price
    percent = 1 - (difference.amount / old_price.amount)
    if percent < Decimal("0.9"):
        raise ValueError("Can't counteroffer by more than 10%")
