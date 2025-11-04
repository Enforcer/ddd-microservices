import pathlib
from typing import Iterator

import alembic
import alembic.config
import pytest
from negotiations.infrastructure.db import engine, session_factory
from sqlalchemy import create_engine, text


@pytest.fixture(scope="session", autouse=True)
def test_db() -> Iterator[None]:
    test_db_name = engine.url.database + "_tests"

    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        connection.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        connection.execute(text(f"CREATE DATABASE {test_db_name}"))

    testing_db_url = engine.url.set(database=test_db_name)
    test_db_engine = create_engine(testing_db_url, future=True, echo=True)
    session_factory.configure(bind=test_db_engine)

    script_location = (
        pathlib.Path(__file__).parent.parent
        / "negotiations/infrastructure/db/migrations/"
    )
    config = alembic.config.Config()
    config.set_main_option("script_location", str(script_location))
    alembic.command.upgrade(config=config, revision="head")
    yield
    test_db_engine.dispose()
