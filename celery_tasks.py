from celery import Celery
from redis_config import redis_client
import logging
import os
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

redis_connection_string = f"redis://{os.environ.get('REDIS_HOST')}:6379/0"
celery = Celery(
    "tasks",
    broker=redis_connection_string,
    backend=redis_connection_string
)


@celery.task
def trigger_webhook(timer_uuid: str, url: str) -> None:
    """
    Sends a POST request with body {'id': timer_uuid} to a URL
    :param timer_uuid: The unique id of the timer
    :param url: URL to which the post request is sent
    :return: None
    """
    logger.info(f"Performing POST call {timer_uuid} to {url}")
    try:
        resp = requests.post(url, json={"id": timer_uuid})
        if resp.ok:
            logging.info(f"Successfully performed POST call to {url}, receiving status {resp.status_code}")
        else:
            logging.error(f"Failed performing POST call to {url}, receiving status {resp.status_code}")
    finally:
        redis_client.hset(timer_uuid, "expires_at", 0) # Ensure this is executed even when request fails
