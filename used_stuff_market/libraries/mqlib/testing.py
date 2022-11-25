import mqlib
from kombu import Queue


def purge(queue) -> None:
    with mqlib.PoolFactory.get().acquire(block=True) as conn:
        queue(conn).purge()


def next_message(queue: Queue, timeout: int = 5) -> dict:
    with mqlib.PoolFactory.get().acquire(block=True) as conn:
        messages = []
        with conn.Consumer(
            queue, callbacks=[lambda body, message: messages.append((body, message))]
        ):
            conn.drain_events(timeout=timeout)

        body, message = messages[0]
        message.ack()  # To remove from queue
        return body
