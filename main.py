from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Scheduler API",
    description="The API for scheduling callbacks",
    version="0.0.1"
)

app.include_router(router)
