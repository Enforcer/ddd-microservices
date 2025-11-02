import pytest

from items.events import ItemUpdated
from mqlib.apicurio_registry_client import ApicurioRegistryClient, IncompatibleVersion


@pytest.fixture()
def schema_registry_client() -> ApicurioRegistryClient:
    return ApicurioRegistryClient()


def test_event_schema_maintains_compatibility(schema_registry_client: ApicurioRegistryClient) -> None:
    new_schema = ItemUpdated.model_json_schema()

    pytest.fail("Incomplete test")


GOLDEN_EVENT_SCHEMA = {
    "$defs": {
        "Price": {
            "properties": {
                "amount": {
                    "title": "Amount",
                    "type": "number"
                },
                "currency": {
                    "title": "Currency",
                    "type": "string"
                }
            },
            "required": [
                "amount",
                "currency"
            ],
            "title": "Price",
            "type": "object"
        }
    },
    "properties": {
        "item_id": {
            "title": "Item Id",
            "type": "integer"
        },
        "title": {
            "title": "Title",
            "type": "string"
        },
        "description": {
            "title": "Description",
            "type": "string"
        },
        "price": {
            "$ref": "#/$defs/Price"
        },
        "version": {
            "title": "Version",
            "type": "integer"
        }
    },
    "required": [
        "item_id",
        "title",
        "description",
        "price",
        "version"
    ],
    "title": "ItemUpdated",
    "type": "object"
}
