import logging

import mqlib
from catalog import dao
from catalog.queues import item_cdc, item_unliked, item_liked, setup_queues


def on_item_change(body: dict, message: mqlib.Message) -> None:
    logging.info("Item CDC: %r", body)
    try:
        version = body["version"]
    except KeyError:
        return

    existing_doc = dao.get(body["item_id"])
    if existing_doc is not None and existing_doc["version"] >= version:
        logging.warning(
            "Duplicate detected for: %r, we're at %d but got version %d",
            body["item_id"],
            existing_doc["version"],
            version,
        )
        return

    if existing_doc is not None:
        likes = existing_doc["likes"]
    else:
        likes = 0

    data = {**body, "likes": likes}
    dao.upsert(body["item_id"], data)


def on_item_liked(body: dict, message: mqlib.Message) -> None:
    item = dao.get(body["item_id"])
    item["likes"] += 1
    dao.upsert(body["item_id"], item)


def on_item_unliked(body: dict, message: mqlib.Message) -> None:
    item = dao.get(body["item_id"])
    item["likes"] -= 1
    dao.upsert(body["item_id"], item)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_queues()
    mqlib.consume(
        {
            item_cdc: on_item_change,
            item_liked: on_item_liked,
            item_unliked: on_item_unliked,
        }
    )
