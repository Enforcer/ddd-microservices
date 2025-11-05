from typing import Iterator

from lagom import Container, context_dependency_definition
from sqlalchemy.orm import Session
from container_or_host import host_for_dependency
from items.app.availability import AvailabilityPort

from items.app.outbox import Outbox
from items.app.repository import ItemsRepository
from items.infrastructure.availability import AvailabilityHttpClient
from items.infrastructure.db import session_factory
from items.infrastructure.outbox import SqlAlchemyOutbox
from items.infrastructure.repository import SqlAlchemyItemsRepository

container = Container()

availability_base_url = f"http://{host_for_dependency("availability")}:8300"
container[AvailabilityPort] = lambda: AvailabilityHttpClient(availability_base_url)
container[ItemsRepository] = SqlAlchemyItemsRepository
container[Outbox] = SqlAlchemyOutbox


@context_dependency_definition(container)
def a_session() -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
