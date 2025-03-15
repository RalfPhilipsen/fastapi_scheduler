from pydantic import BaseModel, HttpUrl

class Timer(BaseModel):
    hours: int
    minutes: int
    seconds: int
    url: HttpUrl
