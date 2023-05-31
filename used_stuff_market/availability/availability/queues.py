import mqlib
from kombu import Queue

resource_registered = Queue("availability.fact.resource_registered", durable=True)
register_resource = Queue("availability.cmd.register_resource", durable=True)

def setup_queues():
    mqlib.declare(resource_registered)
    mqlib.declare(register_resource)
