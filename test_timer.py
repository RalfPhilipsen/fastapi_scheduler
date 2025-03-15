from fastapi.testclient import TestClient
from main import app
from redis_config import redis_client
import time
import uuid


client = TestClient(app=app)


def test_set_timer():
    response = client.post(
        "/timer",
        json={
            "hours": 0,
            "minutes": 0,
            "seconds": 2,
            "url": "http://example.com/webhook"
        },
    )
    data = response.json()

    assert response.status_code == 201
    assert "id" in data
    assert data["time_left"] == 2
    assert redis_client.exists(data["id"])


def test_set_timer_invalid():
    response = client.post(
        "/timer",
        json={
            "hours": 0,
            "minutes": 0,
            "seconds": 0,
            "url": "http://example.com/webhook"
        },
    )
    assert response.status_code == 400


def test_get_recent_timer():
    timer_uuid = str(uuid.uuid4())
    expires_at = int(time.time()) + 5
    redis_client.hset(timer_uuid, mapping={"expires_at": expires_at, "url": "http://example.com/webhook"})

    response = client.get(f"/timer/{timer_uuid}")
    data = response.json()

    assert response.status_code == 200
    assert "time_left" in data
    assert data["time_left"] > 0


def test_get_expired_timer():
    timer_uuid = str(uuid.uuid4())
    redis_client.hset(timer_uuid, mapping={"expires_at": int(time.time()) - 10, "url": "http://example.com/webhook"})

    response = client.get(f"/timer/{timer_uuid}")
    data = response.json()

    assert response.status_code == 200
    assert data["time_left"] == 0


def test_get_non_existent_timer():
    response = client.get(f"/timer/{uuid.uuid4()}")
    assert response.status_code == 404
