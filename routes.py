from fastapi import APIRouter, HTTPException
from schemas.timer_setter_schema import Timer
from schemas.timer_response_schema import TimerResponse
from redis_service import store_webhook_in_redis, get_timer_seconds
import uuid


router = APIRouter(prefix="/timer", tags=["timer"])

@router.post(path="",
             status_code=201,
             response_model=TimerResponse)
def set_timer(timer: Timer):
    total_seconds = timer.hours * 3600 + timer.minutes * 60 + timer.seconds
    if total_seconds <= 0:
        raise HTTPException(status_code=400, detail="Timer must be greater than zero")

    timer_uuid = str(uuid.uuid4())
    store_webhook_in_redis(timer_uuid, total_seconds, timer.url)

    return {"id": timer_uuid, "time_left": total_seconds}


@router.get(path="/{timer_uuid}",
            response_model=TimerResponse)
def get_timer(timer_uuid: str):
    seconds_left = get_timer_seconds(timer_uuid)
    return {"id": timer_uuid, "time_left": seconds_left}
