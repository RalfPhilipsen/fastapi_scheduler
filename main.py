from fastapi import FastAPI
from schemas.set_timer_schema import Timer

app = FastAPI(
    title="Scheduler API",
    description="The API for scheduling callbacks",
    version="0.0.1"
)


@app.post(path="/timer",
          tags=["timer"],
          status_code=201)
async def set_timer(timer: Timer):
    print(timer)


@app.get(path="/timer/{timer_uuid}",
         tags=["timer"])
async def get_timer(timer_uuid: str):
    print(timer_uuid)
