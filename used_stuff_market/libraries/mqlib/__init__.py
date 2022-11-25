from typing import Protocol, TypedDict

from container_or_host import host_for_dependency
from kombu import Connection, Exchange, Queue
from kombu.connection import ConnectionPool
from kombu.pools import connections

__all__ = ["publish", "declare", "consume", "Message"]


HOST = host_for_dependency(addres_for_docker="rabbitmq")
BROKER_URL = f"amqp://guest:guest@{HOST}//"


class PoolFactory:
    _pool: ConnectionPool | None = None

    @classmethod
    def get(cls) -> ConnectionPool:
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

    def ack(self) -> None:
        ...

    def reject(self) -> None:
        ...


class ConsumptionCallback(Protocol):
    def __call__(self, body: dict, message: Message) -> None:
        ...


def consume(callback: ConsumptionCallback, *queues: Queue) -> None:
    with PoolFactory.get().acquire(block=True) as conn:
        with conn.Consumer(list(queues), callbacks=[callback]):
            while True:
                try:
                    conn.drain_events()
                except KeyboardInterrupt:
                    return
