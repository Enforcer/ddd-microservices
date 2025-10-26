from typing import Iterator

import pytest
from catalog import db, migrations


@pytest.fixture(scope="session", autouse=True)
def test_db() -> Iterator[None]:
    db.DATABASE = "catalog_tests"
    migrations.migrate()
    yield
    db.get().client.drop_database(db.DATABASE)
