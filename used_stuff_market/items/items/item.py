from decimal import Decimal

import attr


@attr.s(auto_attribs=True)
class Item:
    id: int = attr.ib(init=False)
    owner_id: int
    title: str
    description: str
    starting_price_amount: Decimal
    starting_price_currency: str
