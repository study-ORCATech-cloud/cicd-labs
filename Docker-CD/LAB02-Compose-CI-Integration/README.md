# LAB02: Managing Multi-Container Applications with Docker Compose

Building on Lab 01, this lab introduces **Docker Compose**, a powerful tool for defining and running multi-container Docker applications locally. You'll create a simple web application that uses a Python Flask frontend and a Redis backend for a hit counter, and define these services in a `docker-compose.yml` file.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand the purpose and basic syntax of a `docker-compose.yml` file.
- Define a multi-container application with a web service (Python Flask) and a database service (Redis).
- Use Docker Compose to build, run, test, and manage these services locally.
- Understand how services in Docker Compose can communicate with each other over a Docker network.

---

## 🧰 Prerequisites

-   **Completion of Docker-CD Lab 01:** Or a good understanding of `Dockerfile` basics.
-   **Docker and Docker Compose Installed:** Ensure both are installed and running. Docker Desktop includes Compose. For Linux, you might need to install Docker Compose separately. Verify with `docker --version` and `docker-compose --version` (or `docker compose version` for newer versions).
-   **Basic Terminal/Command Line Knowledge.**
-   **Text Editor/IDE.**

---

## 📂 Folder Structure for This Lab

```bash
Docker-CD/LAB02-Compose-CI-Integration/
├── app/                            # Python Flask application with Redis
│   ├── Dockerfile                  # Dockerfile for the web app (COMPLETE)
│   ├── main.py                     # Flask app logic with Redis counter (COMPLETE)
│   ├── requirements.txt            # Python dependencies (Flask, redis) (COMPLETE)
│   └── tests/
│       └── test_main.py            # Basic unit tests for main.py (COMPLETE)
├── docker-compose.yml              # Docker Compose definition (contains TODOs)
├── README.md                       # Lab instructions (this file)
└── solutions.md                    # Completed docker-compose.yml
```

--- 

## 🐍 The Sample Python Flask & Redis Application (`app/`)

The `app/` directory contains a Python web application that:
- Uses Flask to serve a webpage.
- Connects to a Redis service (expected to be named `redis`).
- Increments a 'hits' counter in Redis each time the main page is visited and displays the count.
- Has a `/health` endpoint to check its own status and connection to Redis.
- Includes a `Dockerfile` to containerize itself.
- Has basic unit tests in `app/tests/test_main.py` that will be run by `pytest`.

**You do NOT need to modify the code in the `app/` directory. It is provided as a complete example.** Your focus is on `docker-compose.yml`.

---

## 🐳 Defining and Running a Multi-Container Application with `docker-compose.yml`

Docker Compose uses a YAML file (typically `docker-compose.yml`) to configure application services. This allows you to define, build, and run multiple containers as a single application.

Your task is to complete the `docker-compose.yml` file in the root of the `LAB02-Compose-CI-Integration` directory.

**1. Understanding `docker-compose.yml` Structure:**

*   `version`: Specifies the Docker Compose file format version.
*   `services`: Defines the different containers that make up your application.
    *   Each service has a name (e.g., `web`, `redis`).
    *   `build`: Specifies the build context (and optionally Dockerfile) for a service if it needs to be built from a Dockerfile.
    *   `image`: Specifies the Docker image to use for a service (e.g., from Docker Hub).
    *   `ports`: Maps ports from the host to the container (e.g., `"8080:80"`).
    *   `environment`: Sets environment variables inside the container.
    *   `depends_on`: Defines service dependencies, controlling startup order.
    *   `volumes`: Mounts host paths or named volumes into the container.
*   `volumes` (top-level): Declares named volumes for persistent data.

**2. Complete the `TODO` items in `docker-compose.yml`:**

   Open `docker-compose.yml`. It contains `TODO`s guiding you to define two services: `web` and `redis`.

   *   **`TODO_WEB_SERVICE`:**
        *   **`build`**: Point to the `app/` directory where the web app's `Dockerfile` is.
        *   **`ports`**: Map host port `5002` (or any available port on your host) to container port `5000` (where Flask runs).
        *   **`environment`**: Set `REDIS_HOST=redis` so the Flask app knows how to find the Redis service.
        *   **`depends_on`**: Make `web` depend on `redis`.

   *   **`TODO_REDIS_SERVICE`:**
        *   **`image`**: Use an official Redis image, like `redis:6-alpine` or `redis:latest`.
        *   *(Optional)* You can expose port `6379` if you want to connect to Redis from your host for debugging, but it's not strictly necessary for the app to work as the `web` service will connect to `redis` over the internal Docker network.

**3. Test Locally with Docker Compose:**

   Navigate to `Docker-CD/LAB02-Compose-CI-Integration/` in your terminal.

   *   **Build and run services:**
        ```bash
        docker-compose up --build -d
        ```
        *   `--build`: Forces Docker Compose to build the images (especially for your `web` service).
        *   `-d`: Runs in detached mode.
   *   **Check running services:**
        ```bash
        docker-compose ps
        ```
        You should see both `web` and `redis` services running.
   *   **Access the web app:** Open your browser to `http://localhost:5002` (or the host port you chose). You should see the hit counter working.
   *   **View logs:**
        ```bash
        docker-compose logs web
        docker-compose logs redis
        ```
   *   **Run unit tests (this is a form of local CI check!):**
        ```bash
        docker-compose run --rm web pytest tests/
        ```
        *   `docker-compose run --rm web ...`: Runs a one-off command in a new `web` service container. `--rm` removes the container after execution. `pytest tests/` is the command to run inside the container. This demonstrates how Docker Compose can be used for running test suites against your services.
   *   **Stop services:**
        ```bash
        docker-compose down
        ```

---

## ✅ Validation Checklist

**Local Docker Compose:**
- [ ] `docker-compose.yml` is correctly defined with `web` and `redis` services.
- [ ] `docker-compose up --build -d` successfully starts both services.
- [ ] The `web` service is accessible in a browser (e.g., at `http://localhost:5002`), and the hit counter increments on refresh.
- [ ] `docker-compose run --rm web pytest tests/` executes successfully, showing passing tests.
- [ ] `docker-compose down` stops and removes the containers.

---

## 🧹 Cleanup

**Local:**
- If services are running locally, run: `docker-compose down`
- You can also remove the built images if desired (though they might be reused):
  ```bash
  docker image rm <image_id_or_name_for_web_service>
  # The redis image is from Docker Hub, so no need to remove it unless you specifically want to clean up all unused images.
  # docker image prune -a # (Careful with this, removes ALL unused images)
  ```

---

## 🧠 Key Concepts Review

-   **Docker Compose**: A tool for defining and running multi-container Docker applications using a YAML file.
-   **`docker-compose.yml`**: The default configuration file for Docker Compose.
    -   **`services`**: Defines the individual containers (e.g., web server, database, cache).
    -   **`build` vs. `image`**: `build` creates an image from a Dockerfile; `image` pulls a pre-built image.
    -   **Networking**: Docker Compose sets up a default network for your application, allowing services to discover and communicate with each other using their service names as hostnames (e.g., `web` can reach `redis` at `http://redis:6379`).
    -   **`depends_on`**: Controls the startup order of services (but doesn't guarantee the dependent service is fully *ready*, only that it has *started*).
-   **`docker-compose up`**: Builds (if necessary), creates, starts, and attaches to containers for an application.
-   **`docker-compose build`**: Builds or rebuilds images for services.
-   **`docker-compose run <service> <command>`**: Runs a one-off command on a service. It starts the specified service and any it depends on, executes the command, and then stops the service (but not dependencies started just for it, unless `--rm` is used effectively). This is a key command for using Docker Compose for local CI tasks like running tests.
-   **`docker-compose down`**: Stops and removes containers, networks, and optionally volumes created by `up`.
-   **Local CI with Docker Compose**: Using commands like `docker-compose run` to execute tests or other checks against your services in a consistent, containerized environment directly on your local machine.

---

## 🔁 What's Next?

With Docker Compose, you're now managing multi-container applications more effectively and can even run basic CI checks locally.

Proceed to **[../LAB03-Compose-Dev-Environments/README.md](../LAB03-Compose-Dev-Environments/)** to explore how Docker Compose can further enhance local development environments with features like live code reloading.