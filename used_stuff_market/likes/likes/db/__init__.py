from contextlib import contextmanager
from typing import Any

from container_or_host import host_for_dependency
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    as_declarative,
    registry,
    scoped_session,
    sessionmaker,
)

HOST = host_for_dependency(addres_for_docker="postgresdb")
engine = create_engine(
    f"postgresql://usf:usf@{HOST}:5432/likes", future=True, echo=True
)
session_factory = sessionmaker(bind=engine)
ScopedSession = scoped_session(session_factory)


@as_declarative()
class Base:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


metadata = Base.metadata  # type: ignore
mapper_registry = registry(metadata=metadata)


@contextmanager
def db_session() -> Session:
    session = ScopedSession()
    try:
        yield session
    except Exception:
        raise
    finally:
        ScopedSession.remove()
