# LAB07: Simulating a Microservices CI Pipeline Locally with Docker Compose

When developing applications composed of multiple microservices, it's essential to have a process for building, testing, and integrating them reliably. While full-fledged CI/CD platforms offer extensive automation, you can simulate many core CI (Continuous Integration) pipeline stages locally using just Docker Compose. This lab demonstrates how to structure a multi-service application and use Docker Compose to manage build and test stages for each service, as well as run them together for interaction testing.

This approach helps ensure that individual services are working correctly and that they integrate as expected, all within your local development environment using familiar Docker tools.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand how to structure a multi-service application with individual Dockerfiles and tests.
- Define services in Docker Compose for both running applications and executing tests.
- Use Docker Compose commands to simulate a CI pipeline locally:
    - Build service images.
    - Run unit tests for each service in isolation within its Docker environment.
    - Run all services together for manual interaction testing or to prepare for integration tests.
- Understand how to use `docker-compose run --rm <service_name>` effectively for one-off tasks like running tests.

---

## 🧰 Prerequisites

- Completion of Docker-CD Labs 01-06 (understanding of `Dockerfile`, `docker-compose.yml`, health checks).
- Docker and Docker Compose installed.
- Basic Python and Flask knowledge.
- Basic terminal/command-line knowledge.
- A text editor/IDE.

---

## 📂 Folder Structure for This Lab

```bash
Docker-CD/LAB07-Microservices-CI-Pipeline/
├── api_service/                    # First microservice (Flask API)
│   ├── Dockerfile                  # Dockerfile for the API service (COMPLETE)
│   ├── app.py                      # Flask application code for API (COMPLETE)
│   ├── requirements.txt            # Python dependencies (Flask, pytest) (COMPLETE)
│   └── tests/
│       └── test_app.py             # Unit tests for the API service (COMPLETE)
├── web_frontend_service/           # Second microservice (Flask Web App)
│   ├── Dockerfile                  # Dockerfile for the Web Frontend (COMPLETE)
│   ├── app.py                      # Flask application code for Web Frontend (COMPLETE)
│   ├── requirements.txt            # Python dependencies (Flask, requests, pytest) (COMPLETE)
│   └── tests/
│       └── test_app.py             # Unit tests for the Web Frontend (COMPLETE)
├── docker-compose.yml              # Contains TODOs for service definitions and test runners
├── README.md                       # Lab instructions (this file)
└── solutions.md                    # Completed docker-compose.yml
```

---

## ⚙️ The Microservices

This lab uses two simple Flask-based microservices:

1.  **`api_service`**: A basic API that provides a `/data` endpoint and a `/health` endpoint.
2.  **`web_frontend_service`**: A web application that fetches data from the `api_service` and displays it. It also has its own `/health` endpoint that checks its own status and the reachability of the `api_service`.

Both services include their own `Dockerfile`, `requirements.txt`, and a `tests/` directory containing unit tests written with `pytest`.

--- 

## ✨ Part 1: Defining Services for Running and Testing

Your main task is to complete the `docker-compose.yml` file. You will define configurations for:
1.  Running the `api_service` and `web_frontend_service` as standard services.
2.  Special "runner" services (e.g., `api_service_runner`, `web_frontend_service_runner`) whose purpose is solely to execute the unit tests for their respective microservices.

**Open `docker-compose.yml` and complete the following `TODO` items:**

1.  **`TODO_API_SERVICE_DEFINITION`**: 
    *   Configure the `api_service`.
    *   Set its `build` context to `./api_service`.
    *   Assign an appropriate `image` name (e.g., `docker-cd-lab07-api-service`).
    *   Map a host port (e.g., `5010`) to its container port (`5000` by default for this app).
    *   (Recommended) Add a `healthcheck` as learned in Lab 06.

2.  **`TODO_WEB_FRONTEND_SERVICE_DEFINITION`**: 
    *   Configure the `web_frontend_service`.
    *   Set its `build` context to `./web_frontend_service`.
    *   Assign an `image` name (e.g., `docker-cd-lab07-web-frontend`).
    *   Map a host port (e.g., `5011`) to its container port (`5001` by default for this app).
    *   Set the `API_SERVICE_URL` environment variable to point to the `api_service` (e.g., `http://api_service:5000`).
    *   Configure `depends_on` to ensure `api_service` starts (and ideally is healthy) before `web_frontend_service`.
    *   (Recommended) Add a `healthcheck`.

3.  **`TODO_API_SERVICE_TEST_RUNNER`**: 
    *   Define a new service (e.g., `api_service_runner` or `api_tests`).
    *   Its `build` context should be the same as `api_service` (`./api_service`).
    *   The key part is to override the `command`. Instead of running the Flask app, this service should execute the unit tests using `pytest`. The `tests` directory is at the root of the `WORKDIR` in the `api_service/Dockerfile`. So, a command like `pytest -v tests/` should work. Refer to the generic example structure in the `TODO` comment.

4.  **`TODO_WEB_FRONTEND_SERVICE_TEST_RUNNER`**: 
    *   Define another new service (e.g., `web_frontend_service_runner` or `frontend_tests`).
    *   Its `build` context will be `./web_frontend_service`.
    *   Override its `command` to run its `pytest` tests (e.g., `pytest -v tests/`).

--- 

## 🚀 Part 2: Simulating CI Stages with Docker Compose Commands

Once your `docker-compose.yml` is complete, you can simulate a local CI pipeline by running a sequence of Docker Compose commands.

**1. Build All Service Images:**
   This step is akin to the "build" stage in a CI pipeline.
   ```bash
   docker-compose build
   ```
   This will build images for `api_service`, `web_frontend_service`, and implicitly for your test runner services since they share build contexts (or have their own if you defined separate images for them).

**2. Run Unit Tests for `api_service`:**
   This simulates the unit testing stage for the first microservice.
   ```bash
   # Replace 'api_service_runner' with the name you gave your test runner service
   docker-compose run --rm api_service_runner 
   ```
   The `run --rm` command starts an instance of the specified service, executes its command (which you configured to be `pytest`), and then removes the container once the tests are complete. Check the output for test results.

**3. Run Unit Tests for `web_frontend_service`:**
   Simulates unit testing for the second microservice.
   ```bash
   # Replace 'web_frontend_service_runner' with your chosen name
   docker-compose run --rm web_frontend_service_runner
   ```
   Again, check the output for test success or failure.

**4. Run Services Together for Interaction/Manual Testing:**
   If all tests pass, you can run the services together to manually test their interaction or as a precursor to automated integration tests (which are beyond this lab's scope but would be a next step).
   ```bash
   docker-compose up -d api_service web_frontend_service
   ```
   (The `-d` runs them in detached mode). You can also include health checks as part of `docker-compose up` if defined.
   Access the `web_frontend_service` in your browser (e.g., at `http://localhost:5011`) to see if it successfully fetches data from the `api_service`.

**5. Stop Services:**
   ```bash
   docker-compose down
   ```

**(Optional) Scripting the Simulation:**
For a more pipeline-like feel, you could create a simple shell script (e.g., `run_local_ci.sh`) in the lab directory that runs these commands in sequence and perhaps even checks the exit codes of the test runner commands.

```bash
#!/bin/sh
echo "--- Building services ---"
docker-compose build

echo "--- Running API Service tests ---"
docker-compose run --rm api_service_runner
if [ $? -ne 0 ]; then echo "API tests failed!"; exit 1; fi

echo "--- Running Web Frontend Service tests ---"
docker-compose run --rm web_frontend_service_runner
if [ $? -ne 0 ]; then echo "Web Frontend tests failed!"; exit 1; fi

echo "--- All tests passed! --- CI Simulation Complete ---"
# Optionally, bring up services for manual check
# echo "--- Starting services for manual check ---"
# docker-compose up -d api_service web_frontend_service
```
Make it executable (`chmod +x run_local_ci.sh`) and run it (`./run_local_ci.sh`).

--- 

## ✅ Validation Checklist

- [ ] `docker-compose.yml` defines `api_service` and `web_frontend_service` correctly.
- [ ] `docker-compose.yml` defines test runner services (e.g., `api_service_runner`, `web_frontend_service_runner`) with commands that execute `pytest` for each respective service.
- [ ] `docker-compose build` successfully builds all necessary images.
- [ ] `docker-compose run --rm <api_test_runner_service_name>` executes the `api_service` unit tests, and they pass.
- [ ] `docker-compose run --rm <frontend_test_runner_service_name>` executes the `web_frontend_service` unit tests, and they pass.
- [ ] `docker-compose up api_service web_frontend_service` (or similar) starts both services successfully.
- [ ] The `web_frontend_service` (e.g., at `http://localhost:5011`) correctly displays data fetched from `api_service`.

---

## 🧹 Cleanup

To stop and remove containers, networks, and images created by this lab (be cautious with `--rmi all` if you have other projects):
```bash
docker-compose down # Stops and removes containers and networks
# Optional: To remove images built by this compose file:
# docker-compose down --rmi local 
```

--- 

## 🧠 Key Concepts Review

-   **Multi-Service Applications**: Using Docker Compose to define and manage applications composed of several interconnected services.
-   **Service-Specific Testing**: Running tests for each microservice within its own Dockerized environment.
-   **Simulating CI with Docker Compose**: Leveraging `docker-compose build` and `docker-compose run` to create local build and test stages.
-   **Test Runner Services**: Defining services in `docker-compose.yml` specifically for executing test suites.
-   **`docker-compose run --rm`**: A command ideal for running one-off tasks like tests, as it executes the command in a new container and removes the container upon completion.

--- 

## 🔁 What's Next?

You've now seen how to use Docker Compose to simulate a CI pipeline for a microservices application locally. This forms a strong foundation for understanding more complex, automated CI/CD systems.

Next, consider **[../LAB08-Deploy-To-ECS/README.md](../LAB08-Deploy-To-ECS/)**, which explores taking your Dockerized applications to a cloud environment using AWS ECS. 