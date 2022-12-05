import logging

import mqlib
from catalog import dao
from catalog.queues import item_cdc, setup_queues


def on_item_change(body: dict, message: mqlib.Message) -> None:
    logging.info("Item CDC: %r", body)
    item_id = body["item_id"]
    item = dao.get(item_id)
    if item is not None and item["version"] >= body["version"]:
        logging.warning("Duplicate detected!")
        return

    dao.upsert(item_id=body["item_id"], data=body)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_queues()
    mqlib.consume(
        {
            item_cdc: on_item_change,
        }
    )
