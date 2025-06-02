# Solutions for LAB06: Implementing Service Health Checks

This document provides the completed `docker-compose.yml` and `app/Dockerfile` snippets for LAB06, demonstrating how to configure health checks for services.

---

## ✅ Completed `app/Dockerfile` (with `curl` installation)

Here is the relevant part of `app/Dockerfile` showing the installation of `curl`:

```dockerfile
# Base image: Python 3.9 slim version
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Solution for TODO_INSTALL_CURL: Install curl for the health check.
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "-u", "main.py"]
```

**Key Point for `Dockerfile`:**
-   The `RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*` command ensures `curl` is available in the `web` container for its health check.

---

## ✅ Completed `docker-compose.yml` (with Health Checks)

Here is the `docker-compose.yml` with health checks configured for both `web` and `redis` services:

```yaml
version: '3.8'

services:
  web:
    build:
      context: ./app
      dockerfile: Dockerfile
    image: docker-cd-lab06-web
    ports:
      - "5007:5000"
    environment:
      - FLASK_ENV=development
      - REDIS_HOST=redis
    depends_on:
      redis:
        condition: service_healthy # Web service waits for Redis to be healthy
    
    # Solution for TODO_WEB_HEALTHCHECK:
    healthcheck:
      # Checks the /health endpoint. CMD-SHELL ensures that the `|| exit 1` part is processed by a shell.
      # Alternatively, `["CMD", "curl", "--fail", "http://localhost:5000/health"]` works if curl's --fail option is sufficient.
      test: ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"]
      interval: 15s       # Check every 15 seconds
      timeout: 5s         # Wait up to 5 seconds for the command to complete
      retries: 3          # Allow 3 consecutive failures before marking as unhealthy
      start_period: 30s   # Give the container 30 seconds to start before first health check counts

  redis:
    image: "redis:6-alpine"
    ports:
      - "6385:6379"

    # Solution for TODO_REDIS_HEALTHCHECK:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"] # Uses redis-cli to ping the Redis server
      interval: 10s       # Check every 10 seconds
      timeout: 3s         # Wait up to 3 seconds for the ping
      retries: 3          # Allow 3 consecutive failures

```

**Key Points for `docker-compose.yml`:**

-   **`web` service health check:**
    -   `test: ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"]`: Uses `curl` to check the `/health` endpoint. The `-f` flag makes `curl` fail silently on HTTP errors (returning a non-zero exit code). The `|| exit 1` ensures that if `curl` fails for any reason (not just HTTP error), the test is marked as a failure. `CMD-SHELL` is used here to allow the pipe `||` to work.
    -   `interval`, `timeout`, `retries`, and `start_period` are configured to manage how frequently and patiently the health check is performed.
-   **`redis` service health check:**
    -   `test: ["CMD", "redis-cli", "ping"]`: This is the standard way to check Redis health. `redis-cli ping` returns `PONG` and exits with 0 if successful.
    -   Parameters are set for regular, quick checks.
-   **`depends_on` with `condition: service_healthy`:**
    -   The `web` service now explicitly waits for the `redis` service to pass its health check before starting. This ensures Redis is fully operational when the web application attempts to connect to it.

---

This completes the setup for LAB06. Students can now follow the `README.md` to implement these solutions and observe the behavior of health checks. 