import mqlib
from kombu import Queue

item_cdc = Queue("items.cdc.item", durable=True)
item_added = Queue("items.fact.item_added", durable=True)
resource_registered = Queue("availability.fact.resource_registered", durable=True)
add_catalog_item = Queue("catalog.cmd.add_catalog_item", durable=True)
register_resource = Queue("availability.cmd.register_resource", durable=True)


def setup_queues():
    mqlib.declare(register_resource)
    mqlib.declare(resource_registered)
    mqlib.declare(add_catalog_item)
    mqlib.declare(item_cdc)
    mqlib.declare(item_added)
