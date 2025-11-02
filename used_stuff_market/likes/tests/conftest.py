import pathlib
from typing import Iterator

import alembic
import alembic.config
import httpx
import mqlib
import pytest
from fastapi.testclient import TestClient
from likes.api import app
from likes.db import engine, session_factory
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

    script_location = pathlib.Path(__file__).parent.parent / "likes/db/migrations/"
    config = alembic.config.Config()
    config.set_main_option("script_location", str(script_location))
    alembic.command.upgrade(config=config, revision="head")
    yield
    test_db_engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def test_broker() -> Iterator[None]:
    mqlib.BROKER_URL = f"amqp://guest:guest@{mqlib.HOST}/tests"
    response = httpx.put(
        f"http://{mqlib.HOST}:15672/api/vhosts/tests", auth=("guest", "guest")
    )
    response.raise_for_status()
    yield
    response = httpx.delete(
        f"http://{mqlib.HOST}:15672/api/vhosts/tests", auth=("guest", "guest")
    )
    response.raise_for_status()


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client
