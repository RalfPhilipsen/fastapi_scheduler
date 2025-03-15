from fastapi import HTTPException
import time
from celery_tasks import trigger_webhook
from redis_config import redis_client


def store_webhook_in_redis(timer_uuid: str, total_seconds: int, url: str) -> None:
    expires_at = int(time.time()) + total_seconds
    redis_client.hset(timer_uuid, mapping={"expires_at": expires_at, "url": str(url)})

    trigger_webhook.apply_async((timer_uuid, str(url)), countdown=total_seconds)


def get_timer_seconds(timer_uuid: str) -> int:
    if not redis_client.exists(timer_uuid):
        raise HTTPException(status_code=404, detail=f"Timer {timer_uuid} not found")

    expires_at = int(redis_client.hget(timer_uuid, "expires_at") or 0)
    seconds_left = max(0, expires_at - int(time.time()))

    return seconds_left
