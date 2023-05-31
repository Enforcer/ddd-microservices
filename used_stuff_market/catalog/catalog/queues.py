import mqlib
from kombu import Queue

item_liked = Queue("likes.fact.item_liked", durable=True)
item_unliked = Queue("likes.fact.item_unliked", durable=True)
add_catalog_item = Queue("catalog.cmd.add_catalog_item", durable=True)


def setup_queues():
    mqlib.declare(item_liked)
    mqlib.declare(item_unliked)
    mqlib.declare(add_catalog_item)
