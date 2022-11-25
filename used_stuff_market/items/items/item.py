import attr
from items.money import Money


@attr.s(auto_attribs=True)
class Item:
    id: int = attr.ib(init=False)
    owner_id: int
    title: str
    description: str
    starting_price: Money
