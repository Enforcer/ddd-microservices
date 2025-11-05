from pydantic import BaseModel

from items.app.outbox import Outbox
from sqlalchemy.orm import Session
from opentelemetry import propagate

from items.infrastructure.models import OutboxEntry


class SqlAlchemyOutbox(Outbox):
    def __init__(self, session: Session) -> None:
        self._session = session

    def put(self, queue: str, message: BaseModel) -> None:
        headers: dict[str, str] = {}
        propagate.inject(headers)
        data = message.model_dump(mode="json")
        entry = OutboxEntry(
            queue=queue,
            data=data,
            headers=headers,
        )
        self._session.add(entry)
