from contextlib import asynccontextmanager
from decimal import Decimal
from typing import Iterator, AsyncIterator

from fastapi import Depends, FastAPI, Header, Response
from items.db import db_session
from items.facade import Items
from items.queues import setup_queues
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session


def get_session() -> Iterator[Session]:
    with db_session() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_queues()
    yield


app = FastAPI(dependencies=[Depends(get_session)], lifespan=lifespan)


class Price(BaseModel):
    amount: Decimal
    currency: str


class ItemData(BaseModel):
    title: str
    description: str
    price: Price

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Cool socks",
                "description": "A very nice item",
                "price": {
                    "amount": 10.99,
                    "currency": "USD",
                },
            }
        }
    )


@app.post("/items")
def add(
    data: ItemData,
    user_id: int = Header(),
    session: Session = Depends(get_session),
) -> Response:
    items = Items()
    items.add(
        owner_id=user_id,
        title=data.title,
        description=data.description,
        starting_price_amount=data.price.amount,
        starting_price_currency=data.price.currency,
    )
    session.commit()
    return Response(status_code=204)


@app.put("/items/{item_id}")
def update(
    item_id: int,
    data: ItemData,
    user_id: int = Header(),
    session: Session = Depends(get_session),
) -> Response:
    items = Items()
    items.update(
        owner_id=user_id,
        item_id=item_id,
        title=data.title,
        description=data.description,
        price_amount=data.price.amount,
        price_currency=data.price.currency,
    )
    session.commit()
    return Response(status_code=204)


@app.get("/items")
def get_items(user_id: int = Header()) -> list[dict]:
    items = Items()
    return items.get_items(owner_id=user_id)  # type: ignore
