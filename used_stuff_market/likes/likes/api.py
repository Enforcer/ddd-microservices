from typing import Iterator

from fastapi import Depends, FastAPI, Header, Response
from fastapi.responses import JSONResponse
from likes.db import db_session
from likes.facade import Likes
from likes.queues import setup_queues
from sqlalchemy.orm import Session

app = FastAPI()


@app.on_event("startup")
def initialize() -> None:
    setup_queues()


def get_session() -> Iterator[Session]:
    with db_session() as session:
        yield session


@app.post("/items/{item_id}/likes")
def like(
    item_id: int, user_id: int = Header(), session: Session = Depends(get_session)
) -> Response:
    likes = Likes()
    likes.like(liker=user_id, item_id=item_id)

    session.commit()

    return Response(status_code=201)


@app.delete("/items/{item_id}/likes")
def unlike(
    item_id: int, user_id: int = Header(), session: Session = Depends(get_session)
) -> Response:
    likes = Likes()
    likes.unlike(liker=user_id, item_id=item_id)

    session.commit()

    return Response(status_code=204)


@app.get("/items/{item_id}/likes")
def get_likes_count(item_id: int) -> Response:
    likes = Likes()
    count = likes.count(item_id=item_id)
    return JSONResponse(content={"likes": count})
