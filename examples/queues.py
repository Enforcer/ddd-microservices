# queues.py
from kombu import Queue

import mqlib

order_placed = Queue("orders.events.order_placed", durable=True)


def setup_queues():
    mqlib.declare(order_placed)


# setting up in FastAPI
from fastapi import FastAPI


app = FastAPI()


@app.on_event("startup")
def initialize() -> None:
    setup_queues()
