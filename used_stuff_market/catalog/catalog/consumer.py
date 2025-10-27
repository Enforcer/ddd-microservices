import logging

import mqlib
from catalog import dao
from catalog.queues import item_cdc, setup_queues


def on_item_change(body: dict, message: mqlib.Message) -> None:
    logging.info("Item CDC: %r", body)
    data = {**body, "likes": 0}
    dao.upsert(body["item_id"], data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_queues()
    mqlib.consume(
        {
            item_cdc: on_item_change,
        }
    )
