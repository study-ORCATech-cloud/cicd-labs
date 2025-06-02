# Solutions for LAB03: Efficient Local Development with Docker Compose

This document provides the completed `docker-compose.yml` for LAB03, focusing on setting up an efficient local development environment with live reloading and development-specific configurations.

---

## ✅ Completed `docker-compose.yml` for Development

Here is the `docker-compose.yml` configured for local development:

```yaml
version: '3.8'

services:
  web:
    build: ./app
    ports:
      - "5003:5000" # Host port 5003 mapped to container port 5000
    
    # Solution for TODO_VOLUMES_DEV:
    # Mounts the local ./app directory to /usr/src/app in the container.
    # This allows changes in your local code to be reflected live in the container.
    volumes:
      - ./app:/usr/src/app
    
    # Solution for TODO_ENVIRONMENT_DEV:
    # Sets environment variables for development.
    # - REDIS_HOST tells the Flask app where to find the Redis service.
    # - FLASK_ENV=development enables Flask's debug mode and auto-reloader.
    #   Alternatively, FLASK_DEBUG=1 could be used.
    environment:
      - REDIS_HOST=redis
      - FLASK_ENV=development # Or FLASK_DEBUG=1
      # - FLASK_DEBUG=1 # If you prefer this over FLASK_ENV

    depends_on:
      - redis

  redis:
    image: "redis:6-alpine"
    ports:
      - "6381:6379" # Optional: Exposing Redis on host port 6381
    # volumes:
    #   - redis_lab03_data:/data # Example for persistent Redis data, not required for this lab

# Optional: Define a named volume if you uncommented it for Redis persistence
# volumes:
#   redis_lab03_data:
```

**Key Changes and Why They Matter for Development:**

-   **`volumes: - ./app:/usr/src/app`**:
    *   This is the core of the live-reloading setup. Your local `app` folder (containing `main.py`, `requirements.txt`, etc.) is directly mapped into the `/usr/src/app` folder inside the `web` container (which is its `WORKDIR`).
    *   When you modify a file in your local `./app` directory, that change is instantly seen by the application running inside the container.

-   **`environment: - FLASK_ENV=development`** (or `FLASK_DEBUG=1`):
    *   This environment variable tells Flask to run in development mode.
    *   **Debugger**: If an error occurs, Flask will show a detailed interactive debugger in your browser.
    *   **Auto-Reloader**: Flask's development server will watch for changes in your Python files (via the volume mount) and automatically reload the server, so you don't have to stop/start `docker-compose` for every code change.

-   **`ports: - "5003:5000"`**:
    *   Maps port `5003` on your host machine to port `5000` inside the `web` container. This allows you to access your Flask app by going to `http://localhost:5003` in your browser. The port `5003` is chosen to avoid potential conflicts with Lab02 if it were running on the default `5000` or `5002`.

-   **`depends_on: - redis`**:
    *   Ensures that the `redis` service is started before the `web` service attempts to start, which is good practice as the web app tries to connect to Redis on startup.

With these configurations, you can run `docker-compose up`, edit your Python code in `app/main.py` locally, save the file, and see the changes reflected in your browser almost instantly after the Flask development server reloads.

---

This setup significantly speeds up the development feedback loop when working with containerized applications. 