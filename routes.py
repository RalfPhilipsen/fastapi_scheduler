from fastapi import APIRouter, HTTPException, Depends
from redis_service import RedisService
from schemas.timer_response_schema import TimerResponse
from schemas.timer_setter_schema import Timer
import uuid


router = APIRouter(prefix="/timer", tags=["timer"])

def get_redis_service() -> RedisService:
    return RedisService()


@router.post(path="",
             status_code=201,
             response_model=TimerResponse)
def set_timer(timer: Timer,
              redis_service: RedisService = Depends(get_redis_service)):
    total_seconds = timer.hours * 3600 + timer.minutes * 60 + timer.seconds
    if total_seconds <= 0:
        raise HTTPException(status_code=400, detail=f"Timer must be greater than zero, received {str(total_seconds)}")

    timer_uuid = str(uuid.uuid4())
    redis_service.store_webhook_in_redis(timer_uuid, total_seconds, timer.url)

    return {"id": timer_uuid, "time_left": total_seconds}


@router.get(path="/{timer_uuid}",
            response_model=TimerResponse)
def get_timer(timer_uuid: str,
              redis_service: RedisService = Depends(get_redis_service)):
    seconds_left = redis_service.get_timer_seconds(timer_uuid)
    return {"id": timer_uuid, "time_left": seconds_left}
