import mqlib
from fastapi.testclient import TestClient
from likes.queues import item_liked, item_unliked
from mockito import verify, when


def test_like_can_be_given_and_taken_away(client: TestClient) -> None:
    item_id = 1
    response = client.get(f"/items/{item_id}/likes")
    assert response.status_code == 200
    assert response.json() == {"likes": 0}

    user_id = 2
    with when(mqlib).publish(...):
        response = client.post(
            f"/items/{item_id}/likes", headers={"user-id": str(user_id)}
        )
        assert response.status_code == 201
        verify(mqlib, times=1).publish(item_liked, {"item_id": item_id})

    response = client.get(f"/items/{item_id}/likes")
    assert response.status_code == 200
    assert response.json() == {"likes": 1}

    with when(mqlib).publish(...):
        response = client.delete(
            f"/items/{item_id}/likes", headers={"user-id": str(user_id)}
        )
        assert response.status_code == 204
        verify(mqlib, times=1).publish(item_unliked, {"item_id": item_id})

    response = client.get(f"/items/{item_id}/likes")
    assert response.status_code == 200
    assert response.json() == {"likes": 0}
