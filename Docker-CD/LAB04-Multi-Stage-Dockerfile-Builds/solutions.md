# Solutions for LAB04: Optimizing Images with Multi-Stage Dockerfile Builds

This document provides the completed `Dockerfile.prod` and `docker-compose.prod.yml` for LAB04, demonstrating how to use multi-stage builds to create lean, optimized Docker images.

---

## ✅ Completed `Dockerfile.prod` (Multi-Stage Build)

Here is the complete `Dockerfile.prod` using multi-stage builds:

```dockerfile
# Dockerfile.prod - For creating an optimized production image using multi-stage builds

# --- Builder Stage --- Solution for TODO_BUILDER_STAGE_BASE_IMAGE
# Solution for TODO_BUILDER_BASE: Using python:3.9 as the builder base.
FROM python:3.9 as builder

# Solution for TODO_BUILDER_WORKDIR: Setting builder working directory.
WORKDIR /opt/app_builder

# Solution for TODO_BUILDER_VENV: Creating and setting up path for virtual environment.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Solution for TODO_BUILDER_COPY_REQ: Copying requirements.txt from ./app context.
COPY ./app/requirements.txt .

# Solution for TODO_BUILDER_INSTALL_DEPS: Installing dependencies into the virtual environment.
RUN pip install --no-cache-dir -r requirements.txt

# Solution for TODO_BUILDER_COPY_APP: Copying the entire app directory into the builder stage.
COPY ./app/ .

# Solution for TODO_BUILDER_RUN_TESTS (Optional but Recommended Practice):
# Running pytest. Ensure pytest is in requirements.txt.
RUN pytest tests/


# --- Final Stage --- Solution for TODO_FINAL_STAGE_BASE_IMAGE
# Solution for TODO_FINAL_BASE: Using python:3.9-slim for a smaller final image.
FROM python:3.9-slim as final

# Solution for TODO_FINAL_WORKDIR: Setting final image working directory.
WORKDIR /usr/src/app

# Solution for TODO_FINAL_COPY_VENV: Copying the installed packages from the builder stage's venv.
COPY --from=builder /opt/venv /opt/venv

# Solution for TODO_FINAL_COPY_APP_CODE: Copying only main.py from the builder stage's app code.
# If you had other necessary runtime files like a config.py or a templates/static folder, you would copy them too.
COPY --from=builder /opt/app_builder/main.py .
# Example: If app had templates and static folders:
# COPY --from=builder /opt/app_builder/templates ./templates
# COPY --from=builder /opt/app_builder/static ./static

# Solution for TODO_FINAL_PATH: Adding the virtual environment's bin to PATH.
ENV PATH="/opt/venv/bin:$PATH"

# Solution for TODO_FINAL_EXPOSE_PORT: Exposing port 5000.
EXPOSE 5000

# Solution for TODO_FINAL_CMD: Setting the default command to run the app.
CMD ["python", "-u", "main.py"]
```

**Key Points for `Dockerfile.prod`:**
-   **`FROM python:3.9 as builder`**: Defines the start of the `builder` stage.
-   **Virtual Environment (`/opt/venv`)**: Dependencies are installed into a venv in the `builder` stage. This keeps them isolated.
-   **`RUN pytest tests/`**: An example of running tests within the build process. If these tests fail, the Docker image build fails.
-   **`FROM python:3.9-slim as final`**: Defines the start of the `final` stage, using a much smaller base image.
-   **`COPY --from=builder /opt/venv /opt/venv`**: This is crucial. It copies the *entire virtual environment* (which contains the installed packages from `requirements.txt`) from the `builder` stage to the `final` stage. This brings in all necessary runtime dependencies without the build tools or source code of those dependencies.
-   **`COPY --from=builder /opt/app_builder/main.py .`**: Copies only the essential application file(s) from the `builder` stage. Test files, the full `requirements.txt` (if not needed at runtime), or other development artifacts are left behind.
-   The `final` stage does not include `pytest` or other development/testing libraries unless they were explicitly part of the runtime dependencies copied via the venv and were not just in `requirements.txt` for build-time testing.

---

## ✅ Completed `docker-compose.prod.yml`

Here is the `docker-compose.prod.yml` configured to use `Dockerfile.prod`:

```yaml
version: '3.8'

services:
  # Solution for TODO_WEB_PROD_SERVICE:
  web_prod:
    build:
      context: . # Current directory where Dockerfile.prod is located
      dockerfile: Dockerfile.prod # Specify the production Dockerfile
    image: docker-cd-lab04-web-prod # Unique name for the production image
    ports:
      - "5005:5000" # Mapping host port 5005 to container port 5000
    environment:
      - FLASK_ENV=production # Explicitly set Flask environment to production (disables debug)
      - REDIS_HOST=redis_prod
    depends_on:
      - redis_prod

  # Solution for TODO_REDIS_PROD_SERVICE:
  redis_prod:
    image: "redis:6-alpine"
    ports:
      - "6383:6379" # Optional: Mapping host port 6383 for this Redis instance
```

**Key Points for `docker-compose.prod.yml`:**
-   **`build.context: .`** and **`build.dockerfile: Dockerfile.prod`**: Tells Docker Compose to build an image using `Dockerfile.prod` found in the current directory (`Docker-CD/LAB04-Multi-Stage-Dockerfile-Builds/`).
-   **`image: docker-cd-lab04-web-prod`**: Assigns a clear name to the built production image for easy identification.
-   **`FLASK_ENV=production`**: Ensures the Flask application runs in production mode (debug mode off).
-   No volume mounts for application code are used for `web_prod`, as the optimized code is already baked into the image.

---

By using these configurations, students can build and run a production-like version of their application with a significantly reduced Docker image size, improving efficiency and security. 