from decimal import Decimal

import attr


@attr.s(auto_attribs=True)
class Item:
    id: int = attr.ib(init=False)
    owner_id: int
    title: str
    description: str
    price_amount: Decimal
    price_currency: str
    version_id: int = 1
