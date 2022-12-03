import functools
import logging
import threading
from dataclasses import dataclass
from typing import Protocol, TypedDict

from container_or_host import host_for_dependency
from kombu import Connection, Exchange, Queue
from kombu.connection import ConnectionPool
from kombu.pools import connections
from opentelemetry import propagate, trace

__all__ = ["publish", "declare", "consume", "Message"]


HOST = host_for_dependency(addres_for_docker="rabbitmq")
BROKER_URL = f"amqp://guest:guest@{HOST}//"


tracer = trace.get_tracer(__name__)


class PoolFactory:
    _pool: ConnectionPool | None = None
    _lock = threading.Lock()

    @classmethod
    def get(cls) -> ConnectionPool:
        with cls._lock:
            if cls._pool is None:
                connection = Connection(
                    BROKER_URL, transport_options={"confirm_publish": True}
                )
                cls._pool = connections[connection]
            return cls._pool


ANONYMOUS_EXCHANGE = ""


def publish(
    queue_name_or_queue: str | Queue,
    message: dict,
    headers: dict | None = None,
    exchange: str = ANONYMOUS_EXCHANGE,
) -> None:
    headers = headers or {}
    if isinstance(queue_name_or_queue, Queue):
        queue = queue_name_or_queue.name
    else:
        queue = queue_name_or_queue

    propagate.inject(headers)

    with PoolFactory.get().acquire(block=True) as conn:
        producer = conn.Producer(serializer="json")
        producer.publish(
            message,
            exchange=exchange,
            routing_key=queue,
            headers=headers,
        )


def declare(queue_or_exchange: Exchange | Queue) -> None:
    with PoolFactory.get().acquire(block=True) as conn:
        queue_or_exchange(conn).declare()


class DeliveryInfo(TypedDict):
    consumer_tag: str
    delivery_tag: int
    redelivered: bool
    exchange: str
    routing_key: str


class Message(Protocol):
    headers: dict[str, str]
    properties: dict[str, str]
    delivery_info: DeliveryInfo
    acknowledged: bool

    def ack(self) -> None:
        ...

    def reject(self) -> None:
        ...


class ConsumptionCallback(Protocol):
    def __call__(self, body: dict, message: Message) -> None:
        ...


@dataclass
class Worker:
    thread: threading.Thread
    shutdown_event: threading.Event


def new_consume(consumers: dict[Queue, ConsumptionCallback]) -> None:
    logging.basicConfig()

    workers: list[Worker] = []
    for queue, consumption_callback in consumers.items():
        shutdown_event = threading.Event()

        thread = threading.Thread(
            target=consumer_thread_target,
            kwargs={
                "queue": queue,
                "shutdown_event": shutdown_event,
                "callback": functools.partial(
                    callback,
                    consumption_callback=consumption_callback,
                ),
            },
            daemon=True,
        )
        worker = Worker(thread, shutdown_event)
        workers.append(worker)

    for worker in workers:
        worker.thread.start()

    try:
        for worker in workers:
            worker.thread.join()
    except KeyboardInterrupt:
        logging.info("Shutting down in progress...")
        for worker in workers:
            worker.shutdown_event.set()

    for worker in workers:
        worker.thread.join()

    logging.info("Bye!")


def callback(
    body: dict, message: Message, consumption_callback: ConsumptionCallback
) -> None:
    context = propagate.extract(carrier=message.headers)
    with tracer.start_as_current_span(name="mqlib.consume", context=context):
        consumption_callback(body, message)
        if not message.acknowledged:
            message.ack()


def consumer_thread_target(
    queue: Queue, shutdown_event: threading.Event, callback: ConsumptionCallback
) -> None:
    logging.info("Starting consumption of %r", queue)

    with PoolFactory.get().acquire(block=True) as conn:
        with conn.Consumer([queue], callbacks=[callback]):
            while True:
                if shutdown_event.is_set():
                    break

                try:
                    conn.drain_events(timeout=1)
                except TimeoutError:
                    continue
                except KeyboardInterrupt:
                    return


def consume(callback: ConsumptionCallback, *queues: Queue) -> None:
    with PoolFactory.get().acquire(block=True) as conn:
        with conn.Consumer(list(queues), callbacks=[callback]):
            while True:
                try:
                    conn.drain_events()
                except KeyboardInterrupt:
                    return
