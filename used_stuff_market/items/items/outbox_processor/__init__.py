import logging
import time
from typing import ContextManager

import mqlib
from sqlalchemy.orm import Session
from items.main import container
from items.infrastructure.models import OutboxEntry
from items.infrastructure.queues import setup_queues


def run_once():
    with container.resolve(ContextManager[Session]) as session:
        entries = (
            session.query(OutboxEntry)
            .with_for_update(skip_locked=True)
            .filter(OutboxEntry.retries_left >= 0)
            .order_by(OutboxEntry.when_created)
            .limit(100)
            .all()
        )
        for entry in entries:
            try:
                mqlib.publish(queue_name_or_queue=entry.queue, message=entry.data)
            except Exception as e:
                entries.retries_left -= 1
                logging.exception("Error while publishing OutboxEntry #%d", entry.id)
            else:
                session.delete(entry)

        session.commit()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    setup_queues()

    logging.info("Running Outbox Processor...")
    while True:
        run_once()
        time.sleep(1)


if __name__ == "__main__":
    main()
