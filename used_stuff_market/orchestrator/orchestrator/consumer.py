import logging
from threading import Lock

import mqlib
import tracing
from orchestrator.process_manager import ItemCdcData, ItemAddedData
from orchestrator.repository import AddingNewItemProcessManagerRepository
from orchestrator.queues import setup_queues, resource_registered, item_cdc, item_added


lock = Lock()


def on_item_cdc(body: dict, message: mqlib.Message) -> None:
    logging.info("Item CDC: %r", body)
    with lock:
        repository = AddingNewItemProcessManagerRepository()
        pm = repository.get_or_create(body["item_id"])

        cdc_data = ItemCdcData(**body)
        pm.item_changed(cdc_data)
        repository.update(pm)


def on_item_added(body: dict, message: mqlib.Message) -> None:
    logging.info("Item added: %r", body)

    with lock:
        repository = AddingNewItemProcessManagerRepository()
        pm = repository.get_or_create(body["item_id"])

        item_added_data = ItemAddedData(**body)
        pm.item_added(item_added_data)
        repository.update(pm)

def on_resource_registered(body: dict, message: mqlib.Message) -> None:
    logging.info("Resource registered: %r", body)
    with lock:
        repository = AddingNewItemProcessManagerRepository()
        pm = repository.get_or_create(body["resource_id"])
        pm.resource_registered()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_queues()
    tracing.setup_tracer("Orchestrator-Consumer")
    mqlib.consume(
        {
            resource_registered: on_resource_registered,
            item_cdc: on_item_cdc,
            item_added: on_item_added,
        }
    )
