import logging

import mqlib
import tracing
from orchestrator.queues import setup_queues, some_queue


def on_some_message(body: dict, message: mqlib.Message) -> None:
    logging.info("Got message: %r", body)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_queues()
    tracing.setup_tracer("Orchestrator-Consumer")
    mqlib.consume(
        {
            some_queue: on_some_message,
        }
    )
