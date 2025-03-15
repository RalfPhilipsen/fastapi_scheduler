# Webhook scheduler
This application creates an API that handles timed webhooks, firing a POST request to a specified URL after a determined amount of time.

The stack can de run with Docker and consists of 3 containers:
- scheduler_api: this creates the API calls using FastAPI, accepts client input and stores the webhook events.
- celery_worker: this executes the webhook events when its time has reached.
- redis_server: this cache is used for storing the webhook information.

## How to run with Docker
The configuration for the three containers can be found in docker-compose.yml. For each, feel free to choose a volume as you see fit, or remove volumes entirely.

You can run the stack by opening the CLI in this folder and running:

`docker-compose up -d`

This will automatically build the project and pull the `redis` image. It will then run the API (port 80), the Redis server (port 6379) and the Celery worker.

Alternatively, you can build the project beforehand by running:

`docker build -t scheduler_api:latest .`

For more building info, see `Dockerfile`

## How to run tests in Docker
To execute the tests, run:

`docker exec scheduler_api bash -c "pytest"`

## Swagger documentation
Swagger documentation is automatically generated and available under the /docs endpoint.

## Some dependencies to know about

- fastapi: The framework used to build this API.
- uvicorn: The ASGI used to run the server.
- celery: Used for the worker that performs the webhook events.
- redis: Cache used for storing the webhook events data.
- pytest: Used for running the automated tests
- pydantic: Comes with fastapi and is used to validate input
