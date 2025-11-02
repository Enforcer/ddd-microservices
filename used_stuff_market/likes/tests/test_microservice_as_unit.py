from unittest.mock import patch

import jsonschema
import pytest
from starlette.testclient import TestClient

import mqlib


def test_liking_item_publishes_event(client: TestClient) -> None:
    user_id = 1
    item_id = 1
    with patch.object(mqlib, "publish") as mock_publish:
        response = client.post(
            f"/items/{item_id}/likes", headers={"user-id": str(user_id)}
        )
        assert response.status_code == 201
        mock_publish.assert_called_once()
        queue, message = mock_publish.call_args[0]
        assert queue.name == "likes.fact.item_liked"
        try:
            jsonschema.validate(message, ITEM_LIKED_SCHEMA)
        except jsonschema.ValidationError:
            pytest.fail("Message schema validation failed")


ITEM_LIKED_SCHEMA = {
    "properties": {"item_id": {"title": "Item Id", "type": "integer"}},
    "required": ["item_id"],
    "title": "ItemLiked",
    "type": "object",
}
