from pydantic import BaseModel

class TimerResponse(BaseModel):
    id: str
    time_left: int
