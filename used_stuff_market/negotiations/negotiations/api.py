from decimal import Decimal

from fastapi import FastAPI, Header, Response
from negotiations.currency import Currency
from negotiations.negotiation import Negotiation
from negotiations.queues import setup_queues
from negotiations.repository import NegotiationsRepository
from pydantic import BaseModel

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
    repository = NegotiationsRepository()
    negotiation = Negotiation(
        item_id=item_id,
        buyer_id=payload.buyer_id,
        seller_id=payload.seller_id,
        price=payload.price,
        currency=payload.currency,
        waits_for_decision_of=payload.seller_id,
    )
    repository.insert(negotiation)
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
) -> Negotiation | Response:
    repository = NegotiationsRepository()
    negotiation = repository.get(
        buyer_id=buyer_id, seller_id=seller_id, item_id=item_id
    )
    if negotiation.broken_off:
        return Response(status_code=404)

    return negotiation


@app.post("/items/{item_id}/negotiations/counteroffer")
def counteroffer(
    item_id: int, payload: CounterOffer, user_id: int = Header()
) -> Response:
    repository = NegotiationsRepository()
    negotiation = repository.get(
        buyer_id=payload.buyer_id, seller_id=payload.seller_id, item_id=item_id
    )
    negotiation.counteroffer(
        user_id=user_id, price=payload.price, currency=payload.currency
    )
    repository.update(negotiation)
    return Response(status_code=204)


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
    repository = NegotiationsRepository()
    negotiation = repository.get(
        buyer_id=buyer_id, seller_id=seller_id, item_id=item_id
    )
    try:
        negotiation.accept(user_id=user_id)
    except Negotiation.NegotiationConcluded:
        return Response(status_code=422)
    except Negotiation.OnlyWaitingSideCanAccept:
        return Response(status_code=403)
    else:
        repository.update(negotiation)
        return Response(status_code=204)


@app.delete("/items/{item_id}/negotiations")
def break_off(
    item_id: int, buyer_id: int, seller_id: int, user_id: int = Header()
) -> Response:
    repository = NegotiationsRepository()
    negotiation = repository.get(
        buyer_id=buyer_id, seller_id=seller_id, item_id=item_id
    )
    try:
        negotiation.break_off()
    except Negotiation.NegotiationConcluded:
        return Response(status_code=422)
    else:
        repository.update(negotiation=negotiation)
        return Response(status_code=204)
