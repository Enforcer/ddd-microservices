from typing import Iterator

from lagom import Container, context_dependency_definition
from sqlalchemy.orm import Session

from items.app.outbox import Outbox
from items.app.repository import ItemsRepository
from items.infrastructure.db import session_factory
from items.infrastructure.outbox import SqlAlchemyOutbox
from items.infrastructure.repository import SqlAlchemyItemsRepository

container = Container()

container[ItemsRepository] = SqlAlchemyItemsRepository
container[Outbox] = SqlAlchemyOutbox


@context_dependency_definition(container)
def a_session() -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
