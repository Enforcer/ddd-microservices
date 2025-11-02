from pydantic import BaseModel


class Price(BaseModel):
    amount: float
    currency: str


class ItemUpdated(BaseModel):
    item_id: int
    title: str
    description: str
    price: Price
    version: int
