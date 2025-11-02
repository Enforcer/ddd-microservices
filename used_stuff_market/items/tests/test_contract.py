from typing import Iterator

import pytest

from items.app.events import ItemUpdated
from mqlib.apicurio_registry_client import ApicurioRegistryClient, IncompatibleVersion


@pytest.fixture()
def schema_registry_client() -> ApicurioRegistryClient:
    return ApicurioRegistryClient()


@pytest.fixture()
def golden_schema(schema_registry_client: ApicurioRegistryClient) -> Iterator[None]:
    schema_registry_client.register_new_artifact("example", GOLDEN_EVENT_SCHEMA)
    schema_registry_client.set_rule("example", "COMPATIBILITY", "FORWARD")
    yield
    schema_registry_client.unregister_artifact("example")


@pytest.mark.usefixtures("golden_schema")
def test_event_schema_maintains_compatibility(
    schema_registry_client: ApicurioRegistryClient,
) -> None:
    new_schema = ItemUpdated.model_json_schema()

    try:
        schema_registry_client.check_version("example", new_schema)
    except IncompatibleVersion:
        pytest.fail("New schema is incompatible")


GOLDEN_EVENT_SCHEMA = {
    "$defs": {
        "Price": {
            "properties": {
                "amount": {"title": "Amount", "type": "number"},
                "currency": {"title": "Currency", "type": "string"},
            },
            "required": ["amount", "currency"],
            "title": "Price",
            "type": "object",
        }
    },
    "properties": {
        "item_id": {"title": "Item Id", "type": "integer"},
        "title": {"title": "Title", "type": "string"},
        "description": {"title": "Description", "type": "string"},
        "price": {"$ref": "#/$defs/Price"},
        "version": {"title": "Version", "type": "integer"},
    },
    "required": ["item_id", "title", "description", "price", "version"],
    "title": "ItemUpdated",
    "type": "object",
}
