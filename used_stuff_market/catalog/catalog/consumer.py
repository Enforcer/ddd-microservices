import logging

import mqlib
from catalog import dao
from catalog.queues import item_cdc, setup_queues


def on_item_change(body: dict, message: mqlib.Message) -> None:
    logging.info("Item CDC: %r", body)
    dao.upsert(item_id=body["item_id"], data=body)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_queues()
    mqlib.consume(
        {
            item_added: on_name_me,
        }
    )
