import mqlib
from kombu import Queue

item_cdc = Queue("items.cdc.item", durable=True)


def setup_queues():
    mqlib.declare(item_cdc)
