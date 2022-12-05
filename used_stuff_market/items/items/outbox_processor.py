import logging
import time

from items.db import db_session
from items.queues import setup_queues


def run_once():
    with db_session() as session:
        pass


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    setup_queues()

    logging.info("Running Outbox Processor...")
    while True:
        run_once()
        time.sleep(1)


if __name__ == "__main__":
    main()
