# Solutions for LAB05: Managing Secrets and Persistent Data with Docker Compose

This document provides the completed `docker-compose.yml` for LAB05. It also reminds students about the `api_key.txt` file they need to create.

---

## 🔑 `api_key.txt` File

Students need to create an `api_key.txt` file in the `Docker-CD/LAB05-Secrets-And-Volumes/` directory.

Example content for `api_key.txt`:
```text
mySuperSecretApiKey12345
```

**Note:** In a real-world scenario, this file should be added to `.gitignore` and never committed to version control if it contains actual sensitive credentials.

---

## ✅ Completed `docker-compose.yml`

Here is the `docker-compose.yml` with solutions for secrets and named volumes:

```yaml
version: '3.8'

# Solution for TODO_SECRETS_GLOBAL: Defining the global secrets block
secrets:
  api_key_secret:
    file: ./api_key.txt # Sources the secret from this file in the lab directory

services:
  web:
    build:
      context: ./app
      dockerfile: Dockerfile
    image: docker-cd-lab05-web
    ports:
      - "5006:5000"
    environment:
      - FLASK_ENV=development
      - REDIS_HOST=redis
      # - API_KEY_FILE=/run/secrets/api_key_secret # This is the default, so not strictly needed to set here
                                                 # but student could set it to a custom path if they also changed target in secrets section

    # Solution for TODO_WEB_SECRETS: Assigning the secret to the web service
    secrets:
      - source: api_key_secret
        # target: my_custom_secret_path # Optional: if student wants to mount it elsewhere than /run/secrets/api_key_secret
                                      # and updated API_KEY_FILE env var in app/main.py or here.

    # Solution for TODO_WEB_VOLUMES: Mounting a named volume for the app's data
    volumes:
      - app_data:/data # Persists content of /data in the container
    depends_on:
      - redis

  redis:
    image: "redis:6-alpine"
    ports:
      - "6384:6379"
    # Solution for TODO_REDIS_VOLUME: Mounting a named volume for Redis data persistence
    volumes:
      - redis_data:/data # Persists Redis data in the /data directory of the container

# Solution for TODO_VOLUMES_GLOBAL: Defining the named volumes
volumes:
  redis_data:   # Declares the named volume for Redis
  app_data:     # Declares the named volume for the web app's data
```

**Key Points for the Solution:**

-   **Top-level `secrets` block:**
    -   `api_key_secret:` declares a secret.
    -   `file: ./api_key.txt` tells Docker Compose to read the content for `api_key_secret` from the `api_key.txt` file located in the same directory as the `docker-compose.yml` file.
-   **`web` service `secrets` section:**
    -   `secrets: - source: api_key_secret` assigns the globally defined `api_key_secret` to the `web` service. By default, this makes the content of `api_key.txt` available as a file at `/run/secrets/api_key_secret` inside the `web` container.
-   **Top-level `volumes` block:**
    -   `redis_data:` and `app_data:` declare two named volumes. Docker will manage the storage for these volumes on the host machine.
-   **`redis` service `volumes` section:**
    -   `volumes: - redis_data:/data` mounts the `redis_data` named volume into the `/data` directory inside the `redis` container. This is the standard directory where Redis stores its data.
-   **`web` service `volumes` section:**
    -   `volumes: - app_data:/data` mounts the `app_data` named volume into the `/data` directory inside the `web` container. The `app/main.py` is configured to write its counter to `/data/app_counter.txt`.

With these configurations, the API key is securely passed to the web application, and both the Redis data and the web application's file-based counter will persist across container restarts.

---

This completes the setup for LAB05. Students can now follow the `README.md` to implement these solutions and test their understanding of Docker Compose secrets and volumes. 