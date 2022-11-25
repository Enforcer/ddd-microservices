import mqlib
from kombu import Queue

some_queue = Queue("", durable=True)


def setup_queues():
    pass
    # mqlib.declare(some_queue)
