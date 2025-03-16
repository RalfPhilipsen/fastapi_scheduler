from fastapi import APIRouter, HTTPException, Depends
from redis_service import RedisService
from schemas.error_schema import ErrorMessage
from schemas.timer_response_schema import TimerResponse
from schemas.timer_setter_schema import Timer
import os
import uuid


router = APIRouter(prefix="/timer", tags=["Webhook Timer"])

def get_redis_service() -> RedisService:
    return RedisService()


@router.post(path="",
             status_code=201,
             response_model=TimerResponse,
             responses={400: {"model": ErrorMessage}, 500: {"model": ErrorMessage}},
             description='Request to execute a webhook to a URL after the determined amount of time. '
                         'Time should be more than 1 second and less than a year. Returns the id of the timer.')
def set_timer(timer: Timer,
              redis_service: RedisService = Depends(get_redis_service)):
    total_seconds = timer.hours * 3600 + timer.minutes * 60 + timer.seconds
    max_seconds = os.environ.get('MAX_SECONDS')
    if total_seconds <= 0:
        raise HTTPException(status_code=400, detail=f"Timer must be greater than zero, received {str(total_seconds)}")
    elif total_seconds > int(max_seconds):
        raise HTTPException(status_code=400, detail=f"Timer must execute within {max_seconds} seconds")

    timer_uuid = str(uuid.uuid4())
    redis_service.store_webhook_in_redis(timer_uuid, total_seconds, str(timer.url))

    return {"id": timer_uuid, "time_left": total_seconds}


@router.get(path="/{timer_uuid}",
            response_model=TimerResponse,
            responses={404: {"model": ErrorMessage}, 500: {"model": ErrorMessage}},
            description='Request to obtain status of a webhook timer. Returns 0 if fulfilled.')
def get_timer(timer_uuid: str,
              redis_service: RedisService = Depends(get_redis_service)):
    seconds_left = redis_service.get_timer_seconds(timer_uuid)
    return {"id": timer_uuid, "time_left": seconds_left}
