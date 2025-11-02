import mqlib
from kombu import Queue

from items.app.queues import ITEM_CDC

item_cdc = Queue(ITEM_CDC, durable=True)


def setup_queues():
    mqlib.declare(item_cdc)
