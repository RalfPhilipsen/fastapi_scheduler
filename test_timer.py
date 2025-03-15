from fastapi.testclient import TestClient
from main import app
import time
import uuid
from redis_config import redis_client

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
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["time_left"] == 2

    # Check if timer exists in Redis
    timer_uuid = data["id"]
    assert redis_client.exists(timer_uuid)

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
    assert response.json()["detail"] == "Timer must be greater than zero"

def test_get_timer():
    # Create a timer
    timer_uuid = str(uuid.uuid4())
    expires_at = int(time.time()) + 5
    redis_client.hset(timer_uuid, mapping={"expires_at": expires_at, "url": "http://example.com/webhook"})

    # Fetch the timer
    response = client.get(f"/timer/{timer_uuid}")
    assert response.status_code == 200
    data = response.json()
    assert "time_left" in data
    assert data["time_left"] > 0  # Timer should still be running

def test_get_expired_timer():
    # Create an expired timer
    timer_uuid = str(uuid.uuid4())
    redis_client.hset(timer_uuid, mapping={"expires_at": int(time.time()) - 10, "url": "http://example.com/webhook"})

    # Fetch the timer
    response = client.get(f"/timer/{timer_uuid}")
    assert response.status_code == 200
    data = response.json()
    assert data["time_left"] == 0  # Timer should be expired

def test_get_non_existent_timer():
    response = client.get(f"/timer/{uuid.uuid4()}")
    assert response.status_code == 404
