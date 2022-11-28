import pytest
from negotiations import offer_cap
from negotiations.money import Currency, Money


@pytest.mark.parametrize(
    "old_price, new_price",
    [
        [
            Money(amount=10, currency=Currency.USD),
            Money(amount=4, currency=Currency.USD),
        ],
        [
            Money(amount=100, currency=Currency.USD),
            Money(amount=94, currency=Currency.USD),
        ],
    ],
)
def test_check_cap_by_5_usd_raises_exception_for_bigger_differences(
    old_price: Money, new_price: Money
) -> None:
    with pytest.raises(ValueError):
        offer_cap.no_more_than_5_usd(old_price=old_price, new_price=new_price)


@pytest.mark.parametrize(
    "old_price, new_price",
    [
        [
            Money(amount=4, currency=Currency.USD),
            Money(amount=2, currency=Currency.USD),
        ],
        [
            Money(amount=10, currency=Currency.USD),
            Money(amount=5, currency=Currency.USD),
        ],
    ],
)
def test_check_cap_by_5_usd_does_not_raise_exception_for_smaller_or_equal_diff(
    old_price: Money, new_price: Money
) -> None:
    try:
        offer_cap.no_more_than_5_usd(old_price=old_price, new_price=new_price)
    except ValueError:
        pytest.fail("Should not raise an exception")


@pytest.mark.parametrize(
    "old_price, new_price",
    [
        [
            Money(amount=10, currency=Currency.USD),
            Money(amount=4, currency=Currency.USD),
        ],
        [
            Money(amount=100, currency=Currency.USD),
            Money(amount=89, currency=Currency.USD),
        ],
    ],
)
def test_10_percent_cap_raises_exception_for_bigger_difference(
    old_price: Money, new_price: Money
) -> None:
    with pytest.raises(ValueError):
        offer_cap.no_more_than_10_percent(old_price=old_price, new_price=new_price)


@pytest.mark.parametrize(
    "old_price, new_price",
    [
        [
            Money(amount=10, currency=Currency.USD),
            Money(amount=9, currency=Currency.USD),
        ],
        [
            Money(amount=100, currency=Currency.USD),
            Money(amount=90, currency=Currency.USD),
        ],
    ],
)
def test_10_percent_cap_does_not_raise_exception_for_smaller_or_equal_diff(
    old_price: Money, new_price: Money
) -> None:
    try:
        offer_cap.no_more_than_10_percent(old_price=old_price, new_price=new_price)
    except ValueError:
        pytest.fail("Should not raise an exception")
