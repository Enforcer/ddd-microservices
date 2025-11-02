from pydantic import BaseModel

from items.app.outbox import Outbox
from sqlalchemy.orm import Session

from items.infrastructure.models import OutboxEntry


class SqlAlchemyOutbox(Outbox):
    def __init__(self, session: Session) -> None:
        self._session = session

    def put(self, queue: str, message: BaseModel) -> None:
        data = message.model_dump(mode="json")
        entry = OutboxEntry(
            queue=queue,
            data=data,
        )
        self._session.add(entry)
