from typing import Iterator

import httpx
import mqlib
import pytest
from negotiations import db


@pytest.fixture(scope="session", autouse=True)
def test_db() -> Iterator[None]:
    db.DATABASE = "negotiations_tests"
    yield
    db.get().client.drop_database(db.DATABASE)


@pytest.fixture(scope="session", autouse=True)
def test_broker() -> Iterator[None]:
    mqlib.BROKER_URL = f"amqp://guest:guest@{mqlib.HOST}/tests"
    response = httpx.put(
        "http://rabbitmq:15672/api/vhosts/tests", auth=("guest", "guest")
    )
    response.raise_for_status()
    yield
    response = httpx.delete(
        "http://rabbitmq:15672/api/vhosts/tests", auth=("guest", "guest")
    )
    response.raise_for_status()
