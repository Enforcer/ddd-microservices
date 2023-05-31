import logging
from uuid import UUID

import mqlib
import requests
import tracing
from availability.queues import register_resource, setup_queues
from container_or_host import host_for_dependency


def on_register_resource(body: dict, message: mqlib.Message) -> None:
    logging.info("Registering new item: %r", body)
    host = host_for_dependency(addres_for_docker="availability")
    url = f"http://{host}:8300/resources"
    owner_id = UUID(body["owner_id"])
    response = requests.post(
        url,
        json={
            "resource_id": body["resource_id"],
            "owner_id": owner_id.hex,
        },
    )
    if not response.ok:
        logging.error("Failed to register item: %r", body)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_queues()
    tracing.setup_tracer("Availability-Consumer")
    mqlib.consume(
        {
            register_resource: on_register_resource,
        }
    )
