from typing import Iterator

import httpx
import mqlib
import pytest
from negotiations import db, migrations


@pytest.fixture(scope="session", autouse=True)
def test_db() -> Iterator[None]:
    db.DATABASE = "negotiations_tests"
    migrations.migrate()
    yield
    db.get().client.drop_database(db.DATABASE)


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
