from catalog import dao


def test_get_non_existent_item_returns_none() -> None:
    result = dao.get(item_id=1)

    assert result is None


def test_returns_whatever_was_inserted_by_upsert() -> None:
    data = {"participants": 10}
    dao.upsert(item_id=2, data=data)

    result = dao.get(item_id=2)

    assert result == {**data, "item_id": 2}


def test_upserts_overrides_existing_item() -> None:
    data = {"tasks_per_day": 4}
    dao.upsert(item_id=3, data=data)
    dao.upsert(item_id=3, data={"tasks_per_day": 6})

    result = dao.get(item_id=3)

    assert result == {"tasks_per_day": 6, "item_id": 3}
