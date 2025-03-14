from fastapi import FastAPI, HTTPException
from schemas.set_timer_schema import Timer
from celery import Celery
import logging
import redis
import uuid
import time
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
app = FastAPI(
    title="Scheduler API",
    description="The API for scheduling callbacks",
    version="0.0.1"
)

redis_client = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True

)
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

@app.post(path="/timer",
          tags=["timer"],
          status_code=201)
def set_timer(timer: Timer):
    total_seconds = timer.hours * 3600 + timer.minutes * 60 + timer.seconds
    if total_seconds <= 0:
        raise HTTPException(status_code=400, detail="Timer must be greater than zero")

    timer_uuid = str(uuid.uuid4())
    expires_at = int(time.time()) + total_seconds

    redis_client.hset(timer_uuid, mapping={"expires_at": expires_at, "url": str(timer.url)})

    trigger_webhook.apply_async((timer_uuid, str(timer.url)), countdown=total_seconds)

    return {"timer_id": timer_uuid, "time_left": total_seconds}



@app.get(path="/timer/{timer_uuid}",
         tags=["timer"])
def get_timer(timer_uuid: str):
    if not redis_client.exists(timer_uuid):
        raise HTTPException(status_code=404, detail=f"Timer {timer_uuid} not found")

    expires_at = int(redis_client.hget(timer_uuid, "expires_at") or 0)
    seconds_left = max(0, expires_at - int(time.time()))

    return {"timer_id": timer_uuid, "time_left": seconds_left}
