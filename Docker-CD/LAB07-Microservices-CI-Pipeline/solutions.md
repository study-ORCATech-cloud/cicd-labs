# Solutions for LAB07: Simulating a Microservices CI Pipeline Locally with Docker Compose

This document provides the completed `docker-compose.yml` for LAB07, demonstrating how to define services for running a multi-service application and for executing their tests, simulating a local CI pipeline.

---

## ✅ Completed `docker-compose.yml`

Here is the `docker-compose.yml` with definitions for the `api_service`, `web_frontend_service`, and their respective test runner services (`api_service_runner`, `web_frontend_service_runner`). Health checks are also included as a best practice from Lab 06.

```yaml
version: '3.8'

services:
  # Solution for TODO_API_SERVICE_DEFINITION:
  api_service:
    build:
      context: ./api_service
    image: docker-cd-lab07-api-service
    ports:
      - "5010:5000" # Host:Container
    environment:
      - FLASK_ENV=development
      - SERVICE_ID=api_prod_001
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 10s

  # Solution for TODO_WEB_FRONTEND_SERVICE_DEFINITION:
  web_frontend_service:
    build:
      context: ./web_frontend_service
    image: docker-cd-lab07-web-frontend
    ports:
      - "5011:5001" # Host:Container (web_frontend runs on 5001 internally by default)
    environment:
      - FLASK_ENV=development
      - API_SERVICE_URL=http://api_service:5000 # api_service listens on 5000 internally
      - SERVICE_ID=frontend_prod_001
    depends_on:
      api_service:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:5001/health || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 15s # Give a bit more time if it waits for API

  # --- CI Simulation: Test Runner Services ---

  # Solution for TODO_API_SERVICE_TEST_RUNNER:
  api_service_runner:
    build:
      context: ./api_service
    image: docker-cd-lab07-api-service-tester # Optional: can use a different image name
    command: ["pytest", "-v", "tests/"]
    environment:
      - FLASK_ENV=testing # Example: if tests need specific env

  # Solution for TODO_WEB_FRONTEND_SERVICE_TEST_RUNNER:
  web_frontend_service_runner:
    build:
      context: ./web_frontend_service
    image: docker-cd-lab07-web-frontend-tester # Optional: can use a different image name
    command: ["pytest", "-v", "tests/"]
    environment:
      - FLASK_ENV=testing
      # API_SERVICE_URL is already mocked in web_frontend_service/tests/test_app.py, 
      # but could be set here if tests relied on an external mock accessible via network for some reason.
      # - API_SERVICE_URL=http://some-mock-api-for-testing:8080 

# No named volumes explicitly required by the lab tasks, but can be added if needed.
# volumes:
#   my_api_data:
#   my_frontend_data:
```

**Key Points for the Solution:**

-   **Service Definitions (`api_service`, `web_frontend_service`):**
    -   Each service has its `build` context pointing to its respective directory.
    -   `ports` are mapped for external access during manual testing.
    -   `web_frontend_service` uses `API_SERVICE_URL` to connect to `api_service` by its service name (`api_service`) and internal port (`5000`).
    -   `depends_on` with `condition: service_healthy` ensures proper startup order and health of dependencies.
    -   `healthcheck` configurations are included for both services.

-   **Test Runner Services (`api_service_runner`, `web_frontend_service_runner`):**
    -   These services share the same `build` context as their corresponding application services. This means they are built from the same `Dockerfile` and have access to the same codebase and dependencies.
    -   The crucial difference is the `command` override. Instead of running the default `CMD` from the `Dockerfile` (which starts the Flask server), the `command` is set to `["pytest", "-v", "tests/"]`. This executes the unit tests located in the `tests/` directory within the service's container.
    -   Using `docker-compose run --rm api_service_runner` will build (if not already built), create, and start a container for `api_service_runner`, run the `pytest` command, output the results, and then remove the container. The same applies to `web_frontend_service_runner`.
    -   Optional `environment` variables can be set for test runners if the tests require specific configurations (e.g., `FLASK_ENV=testing`).

This `docker-compose.yml` structure allows students to simulate a CI pipeline locally by:
1.  Building all images: `docker-compose build`
2.  Running API tests: `docker-compose run --rm api_service_runner`
3.  Running Frontend tests: `docker-compose run --rm web_frontend_service_runner`
4.  Running the application for manual/interaction testing: `docker-compose up -d api_service web_frontend_service`

---

This completes the setup for LAB07. Students can now follow the `README.md` to implement these solutions and practice simulating a CI pipeline for their microservices using Docker Compose. 