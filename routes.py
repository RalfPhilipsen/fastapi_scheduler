from fastapi import APIRouter, HTTPException
from schemas.set_timer_schema import Timer
from redis_service import store_webhook_in_redis, get_timer_seconds
import uuid
import time

router = APIRouter(prefix="/timer", tags=["timer"])

@router.post(
    path="",
    status_code=201)
def set_timer(timer: Timer):
    total_seconds = timer.hours * 3600 + timer.minutes * 60 + timer.seconds
    if total_seconds <= 0:
        raise HTTPException(status_code=400, detail="Timer must be greater than zero")

    timer_uuid = str(uuid.uuid4())
    expires_at = int(time.time()) + total_seconds
    store_webhook_in_redis(timer_uuid, total_seconds, timer.url)

    return {"timer_id": timer_uuid, "time_left": total_seconds}


@router.get(path="/{timer_uuid}")
def get_timer(timer_uuid: str):
    seconds_left = get_timer_seconds(timer_uuid)
    return {"timer_id": timer_uuid, "time_left": seconds_left}
