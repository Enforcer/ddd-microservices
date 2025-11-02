from typing import Iterator

from lagom import Container, context_dependency_definition
from sqlalchemy.orm import Session

from items.infrastructure.db import session_factory

container = Container()


@context_dependency_definition(container)
def a_session() -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
