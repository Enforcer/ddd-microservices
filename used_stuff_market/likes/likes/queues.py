import mqlib
from kombu import Queue

give_me_name = Queue("give_me_name", durable=True)


def setup_queues() -> None:
    mqlib.declare(give_me_name)
