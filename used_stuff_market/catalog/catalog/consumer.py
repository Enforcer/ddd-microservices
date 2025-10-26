import logging

import mqlib
from catalog import dao
from catalog.queues import item_cdc, item_liked, item_unliked, setup_queues


def on_item_change(body: dict, message: mqlib.Message) -> None:
    logging.info("Item CDC: %r", body)
    item_id = body["item_id"]
    data = dao.get(item_id) or {"likes": 0}
    if data.get("version", 0) != 0 and data["version"] >= body["version"]:
        logging.warning("Duplicate detected!")
        return

    data.update(body)
    dao.upsert(item_id=body["item_id"], data=data)


def on_item_liked(body: dict, message: mqlib.Message) -> None:
    logging.info("Item liked: %r", body)
    item_id = body["item_id"]
    data = dao.get(item_id) or {"likes": 0}
    data["likes"] += 1
    dao.upsert(item_id=body["item_id"], data=data)


def on_item_unliked(body: dict, message: mqlib.Message) -> None:
    logging.info("Item unliked: %r", body)
    item_id = body["item_id"]
    data = dao.get(item_id) or {"likes": 0}
    data["likes"] -= 1
    dao.upsert(item_id=body["item_id"], data=data)


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
