from pydantic import BaseModel

class NegotiationAccepted(BaseModel):
    item_id: int

    class Config:
        allow_mutation = False
