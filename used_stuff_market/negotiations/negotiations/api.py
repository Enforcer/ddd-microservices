from decimal import Decimal

from fastapi import FastAPI, Header, Response
from fastapi.responses import JSONResponse
from negotiations.application import use_cases
from negotiations.application.use_cases import (
    AcceptingNegotiation,
    BreakingOffNegotiation,
    CounterOfferingNegotiation,
    GettingNegotiation,
    StartingNegotiation,
)
from negotiations.domain import exceptions
from negotiations.domain.currency import Currency
from negotiations.domain.money import Money
from negotiations.domain.negotiation import Negotiation
from negotiations.main import deps
from negotiations.queues import setup_queues
from pydantic import BaseModel

app = FastAPI()


@app.on_event("startup")
def initialize() -> None:
    setup_queues()


@app.exception_handler(exceptions.DomainException)
async def http_exception_handler(_request, exc: Exception):
    return JSONResponse(
        {"error_message": "You can't do this", "code": type(exc).__name__},
        status_code=422,
    )


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
    item_id: int,
    payload: NewNegotiation,
    user_id: int = Header(),
    use_case: StartingNegotiation = deps.depends(StartingNegotiation),
) -> Response:
    dto = use_cases.StartingNegotiation.Dto(
        accepting_party_id=user_id,
        item_id=item_id,
        seller_id=payload.seller_id,
        buyer_id=payload.buyer_id,
        starting_price=Money(
            amount=payload.price,
            currency=payload.currency,
        ),
    )
    use_case.run(dto)
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
    item_id: int,
    buyer_id: int,
    seller_id: int,
    user_id: int = Header(),
    use_case: GettingNegotiation = deps.depends(GettingNegotiation),
) -> Negotiation | Response:
    dto = use_cases.GettingNegotiation.Dto(
        requesting_party_id=user_id,
        seller_id=seller_id,
        buyer_id=buyer_id,
        item_id=item_id,
    )
    try:
        result = use_case.run(dto)
    except use_case.RequestedByNonParticipant:
        return Response(status_code=403)
    except use_case.NegotiationNoLongerAvailable:
        return Response(status_code=404)

    return result


@app.post("/items/{item_id}/negotiations/counteroffer")
def counteroffer(
    item_id: int,
    payload: CounterOffer,
    user_id: int = Header(),
    use_case: CounterOfferingNegotiation = deps.depends(CounterOfferingNegotiation),
) -> Response:
    dto = use_cases.CounterOfferingNegotiation.Dto(
        counter_offering_party_id=user_id,
        buyer_id=payload.buyer_id,
        seller_id=payload.seller_id,
        item_id=item_id,
        new_price=Money(amount=payload.price, currency=payload.currency),
    )
    use_case.run(dto)
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
    item_id: int,
    buyer_id: int,
    seller_id: int,
    user_id: int = Header(),
    use_case: AcceptingNegotiation = deps.depends(AcceptingNegotiation),
) -> Response:
    dto = use_case.Dto(
        accepting_party_id=user_id,
        seller_id=seller_id,
        buyer_id=buyer_id,
        item_id=item_id,
    )
    try:
        use_case.run(dto)
    except exceptions.NegotiationConcluded:
        return Response(status_code=422)
    except exceptions.OnlyWaitingSideCanAccept:
        return Response(status_code=403)
    else:
        return Response(status_code=204)


@app.delete("/items/{item_id}/negotiations")
def break_off(
    item_id: int,
    buyer_id: int,
    seller_id: int,
    user_id: int = Header(),
    use_case: BreakingOffNegotiation = deps.depends(BreakingOffNegotiation),
) -> Response:
    dto = use_case.Dto(
        breaking_off_party_id=user_id,
        seller_id=seller_id,
        buyer_id=buyer_id,
        item_id=item_id,
    )
    try:
        use_case.run(dto)
    except exceptions.NegotiationConcluded:
        return Response(status_code=422)
    else:
        return Response(status_code=204)
