from contextlib import contextmanager
from typing import Iterator, Any
from unittest.mock import patch, Mock

import jsonschema
import pytest
from starlette.testclient import TestClient

import mqlib


class Likes:
    def __init__(self, client: TestClient, user_id: int) -> None:
        self._client = client
        self._client.headers["user-id"] = str(user_id)

    def like(self, item_id: int) -> None:
        response = self._client.post(f"/items/{item_id}/likes")
        response.raise_for_status()

    def unlike(self, item_id: int) -> None:
        response = self._client.delete(f"/items/{item_id}/likes")
        response.raise_for_status()

    def number_of_likes(self, item_id: int) -> int:
        response = self._client.get(f"/items/{item_id}/likes")
        return response.json()["likes"]


class MessagesAssertObject:
    def __init__(self, publish_mock: Mock) -> None:
        self._publish = publish_mock

    def assert_one_message_published(self, queue: str, schema: dict[str, Any]) -> None:
        __tracebackhide__ = True

        assert len(self._publish.mock_calls) == 1, (
            f"Expected one published message, but there is {len(self._publish.mock_calls)} instead"
        )
        actual_queue, message = self._publish.call_args[0]

        assert actual_queue.name == queue, (
            f"Expected queue {queue} but {actual_queue.name} was used"
        )

        try:
            jsonschema.validate(message, schema)
        except jsonschema.ValidationError:
            pytest.fail("Message schema validation failed")

    def assert_no_message_published(self) -> None:
        __tracebackhide__ = True

        assert len(self._publish.mock_calls) == 0, (
            f"Expected no published message, but there is/are {len(self._publish.mock_calls)} instead"
        )


@contextmanager
def spy_published_messages() -> Iterator[MessagesAssertObject]:
    with patch.object(mqlib, "publish") as publish_mock:
        yield MessagesAssertObject(publish_mock)


def test_liking_item_bumps_counter(client: TestClient) -> None:
    likes = Likes(client, user_id=1)

    likes.like(item_id=2)

    assert likes.number_of_likes(item_id=2) == 1


def test_liking_item_twice_bumps_counter_once(client: TestClient) -> None:
    likes = Likes(client, user_id=1)

    likes.like(item_id=3)
    likes.like(item_id=3)

    assert likes.number_of_likes(item_id=2) == 1


def test_liking_item_publishes_event(client: TestClient) -> None:
    likes = Likes(client, user_id=1)

    with spy_published_messages() as messages_spy:
        likes.like(item_id=4)

    messages_spy.assert_one_message_published(
        queue="likes.fact.item_liked", schema=ITEM_LIKED_SCHEMA
    )


def test_liking_item_twice_publishes_no_event_the_second_time(
    client: TestClient,
) -> None:
    likes = Likes(client, user_id=1)

    likes.like(item_id=5)
    with spy_published_messages() as messages_spy:
        likes.like(item_id=5)

    messages_spy.assert_no_message_published()


ITEM_LIKED_SCHEMA = {
    "properties": {"item_id": {"title": "Item Id", "type": "integer"}},
    "required": ["item_id"],
    "title": "ItemLiked",
    "type": "object",
}
