from decimal import Decimal
from typing import Iterator

from fastapi import Depends, FastAPI, Header, Response
from items.db import db_session
from items.facade import Items
from pydantic import BaseModel
from sqlalchemy.orm import Session


def get_session() -> Iterator[Session]:
    with db_session() as session:
        yield session


app = FastAPI(dependencies=[Depends(get_session)])


class Price(BaseModel):
    amount: Decimal
    currency: str


class AddItemData(BaseModel):
    title: str
    description: str
    starting_price: Price

    class Config:
        schema_extra = {
            "example": {
                "title": "Cool socks",
                "description": "A very nice item",
                "starting_price": {
                    "amount": 10.99,
                    "currency": "USD",
                },
            }
        }


@app.post("/items")
def add(
    data: AddItemData,
    user_id: int = Header(),
    session: Session = Depends(get_session),
) -> Response:
    items = Items()
    items.add(
        owner_id=user_id,
        title=data.title,
        description=data.description,
        starting_price_amount=data.starting_price.amount,
        starting_price_currency=data.starting_price.currency,
    )
    session.commit()
    return Response(status_code=204)


@app.get("/items")
def get_items(user_id: int = Header()) -> list[dict]:
    items = Items()
    return items.get_items(owner_id=user_id)  # type: ignore
