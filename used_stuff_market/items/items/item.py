from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Item:
    id: int = field(init=False)
    owner_id: int
    title: str
    description: str
    price_amount: Decimal
    price_currency: str
    version_id: int = 1
