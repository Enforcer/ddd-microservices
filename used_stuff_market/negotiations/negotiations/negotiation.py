from pydantic import BaseModel


class Negotiation(BaseModel):
    item_id: int
    seller_id: int
    buyer_id: int
