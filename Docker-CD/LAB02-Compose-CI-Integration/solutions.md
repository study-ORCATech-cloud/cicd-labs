# Solutions for LAB02: Managing Multi-Container Applications with Docker Compose

This document provides the completed `docker-compose.yml` for LAB02. Students should refer to this after attempting to complete the `TODO`s themselves.

---

## ✅ Completed `docker-compose.yml`

Here is the complete and working `docker-compose.yml` for defining the Flask web application and Redis service:

```yaml
version: '3.8'

services:
  # Solution for TODO_WEB_SERVICE:
  web:
    build: ./app  # Specifies that Dockerfile is in the ./app directory
    ports:
      - "5002:5000" # Maps host port 5002 to container port 5000
    environment:
      - REDIS_HOST=redis # Tells the Flask app that Redis is reachable at hostname 'redis'
      # - FLASK_ENV=development # Optional: for development mode features like debugger
    depends_on:
      - redis # Ensures Redis starts before the web app attempts to connect
    # volumes: # Optional: For live reloading during local development (covered in Lab03)
    #   - ./app:/usr/src/app

  # Solution for TODO_REDIS_SERVICE:
  redis:
    image: "redis:6-alpine" # Uses a lightweight official Redis image
    ports:
      - "6380:6379" # Optional: Exposes Redis on host port 6380 for direct access if needed
    # volumes: # Optional: For Redis data persistence (not strictly needed for this lab's hit counter)
    #   - redis_data:/data

# Optional: Define a named volume if you uncommented it for Redis persistence
# volumes:
#   redis_data:
```

**Key Points for `docker-compose.yml`:**
-   The `web` service builds from the `./app` directory, where its `Dockerfile` is located.
-   `REDIS_HOST=redis` is crucial: Docker Compose creates a network where services can reach each other by their service name. So, the `web` container can find Redis at the hostname `redis`.
-   `depends_on` helps with startup order but doesn't guarantee the dependent service is fully initialized and ready to accept connections (more advanced health checks can handle this, covered in later labs).

---

By implementing this `docker-compose.yml` file, students learn how to manage a multi-service application locally with Docker Compose, including building images, running services, and enabling inter-service communication. 