import mqlib
from kombu import Queue

some_queue = Queue("some_queue", durable=True)


def setup_queues():
    mqlib.declare(some_queue)
