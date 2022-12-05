import logging

import mqlib
from catalog import dao
from catalog.queues import item_added, setup_queues


def on_name_me(body: dict, message: mqlib.Message) -> None:
    logging.info("Item added: %r", body)
    ...


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_queues()
    mqlib.consume(
        {
            item_added: on_name_me,
        }
    )
