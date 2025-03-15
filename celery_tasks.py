from celery import Celery
import logging
import requests
from redis_config import redis_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery.task
def trigger_webhook(timer_uuid: str, url: str):
    logger.info(f"Performing POST call to {url}")
    resp = requests.post(url, json={"id": timer_uuid})
    if resp.ok:
        logging.info(f"Successfully performed POST call to {url}, receiving status {resp.status_code}")
    else:
        logging.error(f"Failed performing POST call to {url}, receiving status {resp.status_code}")
    redis_client.hset(timer_uuid, "expires_at", 0)