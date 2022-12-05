import logging
import time

import mqlib
from items.db import db_session
from items.models import OutboxEntry
from items.queues import setup_queues


def run_once():
    with db_session() as session:
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
            except Exception:
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
