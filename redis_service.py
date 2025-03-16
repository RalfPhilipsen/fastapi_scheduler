from celery_tasks import trigger_webhook
from fastapi import HTTPException
from redis_config import redis_client
import time


class RedisService:
    def __init__(self):
        self.redis_client = redis_client


    def store_webhook_in_redis(self, timer_uuid: str, total_seconds: int, url: str) -> None:
        """
        Stores the webhook timer info in Redis cache and schedules worker to execute it
        :param timer_uuid: The unique id of the timer
        :param total_seconds: The amount of seconds after which the task is executed
        :param url: The URL to which the POST request will be sent
        :return: None
        """
        expires_at = int(time.time()) + total_seconds
        self.redis_client.hset(timer_uuid, mapping={"expires_at": expires_at, "url": str(url)})

        trigger_webhook.apply_async((timer_uuid, str(url)), countdown=total_seconds)


    def get_timer_seconds(self, timer_uuid: str) -> int:
        """
        Retrieves the time left until webhook timer executes
        :param timer_uuid: The unique id of the timer
        :return: The amount of seconds left until the task is executed
        """
        if not redis_client.exists(timer_uuid):
            raise HTTPException(status_code=404, detail=f"Timer {timer_uuid} not found")

        expires_at = int(self.redis_client.hget(timer_uuid, "expires_at") or 0)
        seconds_left = max(0, expires_at - int(time.time()))

        return seconds_left
