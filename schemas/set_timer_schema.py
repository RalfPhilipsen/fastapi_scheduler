from pydantic import BaseModel

class Timer(BaseModel):
    hours: int
    minutes: int
    second: int
    url: str
