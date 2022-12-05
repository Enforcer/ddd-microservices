from catalog import db


def upsert(item_id: int, data: dict) -> None:
    collection = getattr(db.get(), "catalog_items")
    collection.replace_one(
        {"item_id": item_id}, dict(data, item_id=item_id), upsert=True
    )


def add_like(item_id: int, liker_id: int) -> None:
    collection = getattr(db.get(), "catalog_items")
    collection.update_one(
        {"item_id": item_id},
        {"$addToSet": {"likes": liker_id}},
        upsert=True,
    )


def remove_like(item_id: int, liker_id: int) -> None:
    collection = getattr(db.get(), "catalog_items")
    collection.update_one(
        {"item_id": item_id},
        {"$pull": {"likes": liker_id}},
        upsert=True,
    )


def get(item_id: int) -> dict | None:
    collection = getattr(db.get(), "catalog_items")
    return collection.find_one({"item_id": item_id}, projection={"_id": False})
