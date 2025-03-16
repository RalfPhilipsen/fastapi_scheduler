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
During the build process, the libraries defined in `requirements.txt` will automatically be installed.

Alternatively, you can build the project beforehand by running:

`docker build -t scheduler_api:latest .`

For more info on how the image is built, see `Dockerfile`

## How to run tests in Docker
To execute the tests, run:

`docker exec scheduler_api bash -c "pytest"`

## Swagger documentation
Swagger documentation is automatically generated and available under the /docs endpoint.


## Assumptions made
- Hours, minutes and seconds are all integers. It assumed that a granularity lower than a seconds is not necessary.
- A maximum timer length is required, as we cannot guarantee to handle anything a million years from now. This will depend on business case, for now it is set to 1 year.

## Some dependencies to know about
- fastapi: The framework used to build this API.
- uvicorn: The ASGI used to run the server.
- celery: Used for the worker that performs the webhook events.
- redis: Cache used for storing the webhook events data.
- pytest: Used for running the automated tests
- pydantic: Comes with fastapi and is used to validate input

## Improvement for running at large-scale production environment
- Set up in a way that is horizontally scalable (e.g. Kubernetes, Azure App Services etc.).
- Set up some kind of Web Application Firewall and DDOS protection to prevent suspicious usage.
- Set up authentication and/or deploy within private network (if possible).
- Create a retry mechanism for the POST request, handling exceptions for e.g. 429 errors. This can help with large amounts of requests.
- For testing functionality, we use a simple Docker Redis container without authentication. For production, use a proper Redis solution such as Redis Cloud or Azure Cache for Redis for better performance, and use authentication and SSL for security.
- The 2 environment variables are now set in `docker-compose.yml`. For production, use a more elaborate way for handling your config and do not store secrets in codebase.
- Monitor your Redis solution to ensure storage doesn't get full and check if the amount of connected clients does not get too high over time.
