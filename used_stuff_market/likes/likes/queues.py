import mqlib
from kombu import Queue

item_liked = Queue("likes.fact.item_liked", durable=True)
item_unliked = Queue("likes.fact.item_unliked", durable=True)


def setup_queues() -> None:
    mqlib.declare(item_liked)
    mqlib.declare(item_unliked)
