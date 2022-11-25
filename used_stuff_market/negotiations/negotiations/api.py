from decimal import Decimal

from fastapi import FastAPI, Header, Response
from negotiations.currency import Currency
from negotiations.queues import setup_queues
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()


@app.on_event("startup")
def initialize() -> None:
    setup_queues()


class NewNegotiation(BaseModel):
    seller_id: int
    buyer_id: int
    price: Decimal
    currency: Currency

    class Config:
        schema_extra = {
            "example": {
                "seller_id": 1,
                "buyer_id": 2,
                "price": "1.99",
                "currency": "USD",
            }
        }


@app.post("/items/{item_id}/negotiations")
def start_negotiation(
    item_id: int, payload: NewNegotiation, user_id: int = Header()
) -> Response:
    return Response(status_code=204)


class CounterOffer(BaseModel):
    seller_id: int
    buyer_id: int
    price: Decimal
    currency: Currency

    class Config:
        schema_extra = {
            "example": {
                "seller_id": 1,
                "buyer_id": 2,
                "price": "1.99",
                "currency": "USD",
            }
        }


@app.get("/items/{item_id}/negotiations")
def get(
    item_id: int, buyer_id: int, seller_id: int, user_id: int = Header()
) -> Response:
    return JSONResponse(status_code=200, content={})


@app.post("/items/{item_id}/negotiations/counteroffer")
def counteroffer(
    item_id: int, payload: CounterOffer, user_id: int = Header()
) -> Response:
    return Response(status_code=200)


class NegotiationToBreakOff(BaseModel):
    seller_id: int
    buyer_id: int

    class Config:
        schema_extra = {
            "example": {
                "seller_id": 1,
                "buyer_id": 2,
            }
        }


@app.post("/items/{item_id}/negotiations/accept")
def accept(
    item_id: int, buyer_id: int, seller_id: int, user_id: int = Header()
) -> Response:
    return Response(status_code=204)


@app.delete("/items/{item_id}/negotiations")
def break_off(
    item_id: int, buyer_id: int, seller_id: int, user_id: int = Header()
) -> Response:
    return Response(status_code=204)
