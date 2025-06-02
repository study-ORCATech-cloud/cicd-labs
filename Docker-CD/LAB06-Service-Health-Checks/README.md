# LAB06: Implementing Service Health Checks in Docker Compose

When running multi-container applications, it's vital to know if your services are not just running, but are actually healthy and operating correctly. Docker Compose allows you to define **health checks** for your services. Docker can then periodically run these checks and report the health status of your containers. If a container becomes unhealthy, Docker can take action, such as restarting it (though restart policies are a separate configuration).

This lab will guide you through adding health checks to both our Python Flask web application and the Redis service.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand the purpose and benefits of health checks in Docker services.
- Define `healthcheck` configurations in a `docker-compose.yml` file for different types of services.
- Implement a health check for a web service using its HTTP endpoint (e.g., `/health`).
- Implement a health check for a Redis service using `redis-cli ping`.
- Understand the different parameters of a health check: `test`, `interval`, `timeout`, `retries`, and `start_period`.
- Use `docker ps` to monitor the health status of your containers.
- Configure service dependencies based on health status (e.g., `condition: service_healthy`).

---

## 🧰 Prerequisites

- Completion of Docker-CD Labs 01-05 (especially understanding of `Dockerfile`, `docker-compose.yml`).
- Docker and Docker Compose installed.
- Basic terminal/command-line knowledge.
- A text editor/IDE.

---

## 📂 Folder Structure for This Lab

```bash
Docker-CD/LAB06-Service-Health-Checks/
├── app/                            # Python Flask application (from Lab05)
│   ├── Dockerfile                  # Standard Dockerfile (contains a TODO to install curl)
│   ├── main.py                     # Flask app logic (has /health endpoint)
│   ├── requirements.txt            # Python dependencies
│   └── tests/
│       └── test_main.py            # Basic unit tests
├── docker-compose.yml              # Contains TODOs for health checks
├── README.md                       # Lab instructions (this file)
└── solutions.md                    # Completed docker-compose.yml and Dockerfile changes
```

---

## 🐍 The Sample Application (`app/`)

We are using the Python Flask and Redis application from the previous lab. 
- The `app/main.py` already has a `/health` endpoint that returns HTTP 200, which is perfect for our web service health check.
- You will need to modify `app/Dockerfile` to install `curl`, which the web health check will use.

--- 

## ✨ Part 1: Understanding Health Check Parameters

A `healthcheck` in `docker-compose.yml` is defined with several key parameters:

-   **`test`**: (Required) The command to run to check health. It can be a string or a list of strings (shell form or exec form). The command must exit with `0` for healthy or `1` for unhealthy.
-   **`interval`**: (Optional) Time between running the check (e.g., `10s`, `1m`). Default is `30s`.
-   **`timeout`**: (Optional) Time to allow the command to run before considering it failed (e.g., `5s`). Default is `30s`.
-   **`retries`**: (Optional) Number of consecutive failures needed to mark the container as `unhealthy`. Default is `3`.
-   **`start_period`**: (Optional) Grace period for the container to start before health checks begin failing it (e.g., `30s`). Failures during this period don't count towards `retries`. Default is `0s`.

--- 

## 🔧 Part 2: Implementing Health Checks

**1. Install `curl` in the Web App Container:**

   The health check for our web service will use `curl` to make an HTTP request to its `/health` endpoint. `curl` might not be present in the base `python:3.9-slim` image.
   *   Open `Docker-CD/LAB06-Service-Health-Checks/app/Dockerfile`.
   *   **`TODO_INSTALL_CURL`**: Follow the `TODO` comment to add the necessary `RUN` command to install `curl` using `apt-get`. Remember to update package lists and clean up to keep the image lean.

**2. Configure Health Checks in `docker-compose.yml`:**

   Open `Docker-CD/LAB06-Service-Health-Checks/docker-compose.yml`. You will find `TODO` items to guide you:

   *   **`TODO_WEB_HEALTHCHECK`**: In the `web` service definition:
        *   Define a `healthcheck` section.
        *   For the `test` command, use `curl` to access `http://localhost:5000/health`. Ensure the command exits with `1` if `curl` fails (e.g., `["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"]` or `["CMD", "curl", "--fail", "http://localhost:5000/health"]`).
        *   Set reasonable values for `interval`, `timeout`, `retries`, and an optional `start_period` (e.g., 30s to give Flask time to start).

   *   **`TODO_REDIS_HEALTHCHECK`**: In the `redis` service definition:
        *   Define a `healthcheck` section.
        *   For the `test` command, use `redis-cli ping`. This command is available in the official Redis images and returns `PONG` (exit code 0) if healthy. The command should be `["CMD", "redis-cli", "ping"]`.
        *   Set appropriate `interval`, `timeout`, and `retries`.

**3. Service Dependency on Health:**

   Notice in the `web` service, `depends_on` is configured like this:
   ```yaml
   depends_on:
     redis:
       condition: service_healthy
   ```
   This tells Docker Compose that the `web` service should only start after the `redis` service has reported a `healthy` status based on its own health check. This is a powerful way to manage startup order for dependent services.

--- 

## 🚀 Part 3: Building, Running, and Validating Health

**1. Build and Run the Services:**

   Once you have completed all the `TODO`s:
   In your terminal, from the `Docker-CD/LAB06-Service-Health-Checks/` directory:
   ```bash
   # Build images (if changed) and start services in detached mode
   docker-compose up --build -d
   ```

**2. Monitor Health Status:**

   *   Use `docker ps` to view the status of your running containers. After a short while (the `start_period` plus some intervals), you should see the health status in the `STATUS` column (e.g., `Up 5 seconds (healthy)`).
     ```bash
     docker ps
     ```
   *   It might initially show `(health: starting)` and then transition to `(healthy)`. If it becomes `(unhealthy)`, Docker might eventually restart it based on restart policies (not configured in this lab, but good to know).

**3. Test the Application:**

   *   Access the web application in your browser: `http://localhost:5007` (or the host port you configured).
   *   The page should load correctly, indicating both services are operational.

**4. Inspect Health Check Logs (Optional):**

   You can get more details about a container's health check history:
   ```bash
   # Get the container ID or name for your web or redis service
   docker ps

   # Inspect the container (replace <container_id_or_name>)
   docker inspect <container_id_or_name> | grep -A5 Health
   ```
   This will show the recent health check logs, including exit codes and output.

--- 

## ✅ Validation Checklist

- [ ] `app/Dockerfile` includes a command to install `curl`.
- [ ] The `web` service in `docker-compose.yml` has a `healthcheck` section correctly configured to use `curl http://localhost:5000/health`.
- [ ] The `redis` service in `docker-compose.yml` has a `healthcheck` section correctly configured to use `redis-cli ping`.
- [ ] All `healthcheck` parameters (`interval`, `timeout`, `retries`, `start_period` where applicable) are set to reasonable values.
- [ ] `docker-compose up --build -d` starts all services.
- [ ] After the initial start-up period, `docker ps` shows both `web` and `redis` containers as `(healthy)`.
- [ ] The web application at `http://localhost:5007` is accessible and functional.
- [ ] The `web` service correctly waits for the `redis` service to be healthy before starting (due to `condition: service_healthy`).

---

## 🧹 Cleanup

To stop and remove containers and networks:
```bash
docker-compose down
```
If you used named volumes in a previous version of your compose file for this lab and want to remove them, add the `-v` flag:
```bash
docker-compose down -v
```

--- 

## 🧠 Key Concepts Review

-   **Health Checks**: Commands run by Docker inside a container to determine if the service is operating correctly.
-   **`healthcheck` Directive**: Used in `docker-compose.yml` or `Dockerfile` to define health check parameters.
-   **Health Status**: Containers can be `starting`, `healthy`, or `unhealthy`.
-   **`condition: service_healthy`**: A `depends_on` condition that makes a service wait for another service to become healthy before starting.
-   **Importance**: Health checks are fundamental for building resilient and self-healing systems, allowing Docker or orchestrators to automatically manage unhealthy containers.

--- 

## 🔁 What's Next?

Understanding health checks is crucial for robust deployments. 

Next, consider **[../LAB07-Microservices-CI-Pipeline/README.md](../LAB07-Microservices-CI-Pipeline/)** to learn about building more complex CI/CD pipelines, potentially incorporating health status as part of deployment validation. 