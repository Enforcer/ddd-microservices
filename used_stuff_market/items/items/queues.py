import mqlib
from kombu import Queue

item_cdc = Queue("items.cdc.item", durable=True)
item_added = Queue("items.fact.item_added", durable=True)


def setup_queues():
    mqlib.declare(item_cdc)
    mqlib.declare(item_added)
