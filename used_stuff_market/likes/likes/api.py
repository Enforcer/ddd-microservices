from contextlib import asynccontextmanager
from typing import Iterator, AsyncIterator

from fastapi import Depends, FastAPI, Header, Response
from fastapi.responses import JSONResponse

import tracing
from likes.db import db_session, engine
from likes.facade import Likes
from likes.queues import setup_queues
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_queues()
    yield


app = FastAPI(lifespan=lifespan)
tracing.setup_tracer("LikesApi", app=app, engine=engine)


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
