from container_or_host import host_for_dependency
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    as_declarative,
    registry,
    sessionmaker,
)

HOST = host_for_dependency(addres_for_docker="postgresdb")
engine = create_engine(
    f"postgresql://usf:usf@{HOST}:5432/negotiations", future=True, echo=True
)
session_factory = sessionmaker(bind=engine)


@as_declarative()
class Base:
    pass


metadata = Base.metadata  # type: ignore
mapper_registry = registry(metadata=metadata)
