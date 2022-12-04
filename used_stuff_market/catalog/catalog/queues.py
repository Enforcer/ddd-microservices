import mqlib
from kombu import Queue

name_me = Queue("items.fact.name_me", durable=True)


def setup_queues():
    mqlib.declare(name_me)
