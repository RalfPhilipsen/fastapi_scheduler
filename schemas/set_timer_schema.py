from pydantic import BaseModel

class Timer(BaseModel):
    hours: int
    minutes: int
    seconds: int
    url: str
