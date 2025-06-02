# LAB04: Optimizing Images with Multi-Stage Dockerfile Builds

In previous labs, we used a single Dockerfile that served well for development and basic runs. However, for production or distribution, it's crucial to have Docker images that are as small and secure as possible. This lab introduces **multi-stage Dockerfile builds**, a powerful technique to create optimized, lean production images by separating build-time dependencies from runtime necessities.

You will learn to construct a `Dockerfile.prod` that uses a builder stage to compile/install dependencies (and optionally run tests) and a final stage that copies only the essential application code and its direct dependencies into a clean, minimal base image.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand the concept and benefits of multi-stage Dockerfile builds.
- Create a `Dockerfile.prod` with distinct builder and final stages.
- Copy artifacts (like a virtual environment and application code) selectively between stages.
- Build a significantly smaller production-ready Docker image compared to a development-focused image.
- Configure and run this production-like image using a separate `docker-compose.prod.yml` file.
- Compare the sizes of development and production images.

---

## 🧰 Prerequisites

-   **Completion of Docker-CD Labs 01-03:** Understanding of `Dockerfile` basics, `docker-compose.yml`, and local development setups with Docker Compose.
-   **Docker and Docker Compose Installed.**
-   **Basic Terminal/Command Line Knowledge.**
-   **Text Editor/IDE.**

---

## 📂 Folder Structure for This Lab

```bash
Docker-CD/LAB04-Multi-Stage-Dockerfile-Builds/
├── app/                            # Python Flask application with Redis (copied from Lab03)
│   ├── Dockerfile                  # Standard/Development Dockerfile (COMPLETE)
│   ├── main.py                     # Flask app logic (COMPLETE, non-dev messages)
│   ├── requirements.txt            # Python dependencies (COMPLETE)
│   └── tests/
│       └── test_main.py            # Basic unit tests (COMPLETE)
├── Dockerfile.prod                 # Multi-stage Dockerfile for production (contains TODOs)
├── docker-compose.yml              # For running the app with the DEV Dockerfile (COMPLETE, for comparison)
├── docker-compose.prod.yml         # For running the app with Dockerfile.prod (contains TODOs)
├── README.md                       # Lab instructions (this file)
└── solutions.md                    # Completed Dockerfile.prod and docker-compose.prod.yml
```

--- 

## 🐍 The Sample Application (`app/`)

The `app/` directory contains the familiar Python Flask and Redis hit-counter application. 
-   The `app/main.py` has been updated to show generic messages (no "(Dev Mode)" indicators).
-   The `app/Dockerfile` is the *development* Dockerfile we've seen before, useful for quick iteration with tools like `pytest` readily available in the image if installed via `requirements.txt`.
-   Your focus will be on creating `Dockerfile.prod` and `docker-compose.prod.yml` in the lab's root directory.

---

## ✨ Part 1: Creating a Multi-Stage `Dockerfile.prod`

A multi-stage build uses multiple `FROM` instructions in a single Dockerfile. Each `FROM` instruction can use a different base, and begins a new stage of the build. You can selectively copy artifacts from one stage to another, leaving behind everything you don't want in the final image.

**Benefits:**
-   **Smaller Images:** Exclude build tools, development dependencies, source code (if compiled), and intermediate files from the final image.
-   **Improved Security:** Fewer packages and files in the final image mean a smaller attack surface.
-   **Better Build Cache Utilization:** Changes in one stage might not invalidate the cache for subsequent stages if dependencies are managed well.
-   **Clearer Build Logic:** Separates build environment from runtime environment.

**1. Examine `Dockerfile.prod`:**

   Open `Dockerfile.prod` in the lab's root directory. It contains `TODO`s to guide you through creating two stages:
    *   A **`builder` stage**: This stage will be based on a standard Python image. It will set up a virtual environment, install all dependencies (including `pytest` from `app/requirements.txt`), copy the application code, and (optionally, but good practice) run tests.
    *   A **`final` stage**: This stage will be based on a very minimal Python image (e.g., `python:3.9-slim`). It will copy the created virtual environment (with only runtime dependencies) and the necessary application code (e.g., `main.py`) from the `builder` stage. It will *not* include `pytest` or other build-time tools if they were only needed in the builder.

**2. Complete the `TODO` items in `Dockerfile.prod`:**

   Follow the comments and hints in `Dockerfile.prod` to implement both stages.
   *   **Key `TODO`s for `builder` stage:** Define base image, working directory, create virtual environment, copy `app/requirements.txt`, install dependencies, copy `app/` code, and consider adding a step to run `pytest tests/`.
   *   **Key `TODO`s for `final` stage:** Define a slim base image, working directory, copy the virtual environment from the `builder` stage using `COPY --from=builder ...`, copy only essential application files (like `main.py`) from the `builder` stage, set the `PATH` to use the venv, expose the port, and set the `CMD`.

---

## 🐳 Part 2: Configuring `docker-compose.prod.yml`

Now, you'll create a Docker Compose file specifically for building and running your application using the optimized `Dockerfile.prod`.

**1. Examine `docker-compose.prod.yml`:**

   Open `docker-compose.prod.yml` in the lab's root. It has `TODO`s for defining `web_prod` and `redis_prod` services.

**2. Complete the `TODO` items in `docker-compose.prod.yml`:**

   *   **`web_prod` service:**
        *   **`TODO_WEB_PROD_SERVICE`**: Configure this service to:
            *   Build using `Dockerfile.prod` (context should be `.`, and specify `dockerfile: Dockerfile.prod`).
            *   Assign a unique image name (e.g., `yourname/app-prod:lab04`).
            *   Map a host port (e.g., `5005`) to the container's port `5000`.
            *   Set `REDIS_HOST=redis_prod`.
            *   Optionally set `FLASK_ENV=production` (though Flask defaults to no debug mode if `FLASK_DEBUG` or `FLASK_ENV=development` are not set).
            *   Depend on `redis_prod`.
   *   **`redis_prod` service:**
        *   **`TODO_REDIS_PROD_SERVICE`**: Configure this service to use a standard `redis:alpine` image and optionally map a distinct port (e.g., `6383`) for its Redis instance.

---

## 🚀 Part 3: Building, Running, and Comparing Images

**1. Build and Run the Development Version (for comparison):**

   The lab includes a standard `docker-compose.yml` that uses `app/Dockerfile` (the development Dockerfile). This setup includes a volume mount for live reloading and runs Flask in development mode.

   In your terminal, from the `Docker-CD/LAB04-Multi-Stage-Dockerfile-Builds/` directory:
   ```bash
   # Build (if not already built or changed) and run the DEV version
   docker-compose up --build -d web_dev redis_dev
   ```
   Access it at `http://localhost:5004`.
   Take note of the image name (e.g., `docker-cd-lab04-web-dev`) specified in `docker-compose.yml`.

**2. Build and Run the Production Version:**

   Now, build and run using your new `docker-compose.prod.yml`:
   ```bash
   # Build (using Dockerfile.prod) and run the PROD version
   docker-compose -f docker-compose.prod.yml up --build -d web_prod redis_prod
   ```
   Access it at `http://localhost:5005` (or the port you configured).
   Take note of the image name (e.g., `yourname/app-prod:lab04` or whatever you set in `docker-compose.prod.yml`).

**3. Compare Image Sizes:**

   Use the `docker images` command to list your Docker images. Find the development image and the production image you just built. Compare their sizes.
   ```bash
   docker images
   ```
   You should see a significant size reduction for the image built with `Dockerfile.prod`!

**4. Test Functionality:**
   Ensure both the dev (`http://localhost:5004`) and prod (`http://localhost:5005`) versions of the application are working correctly (i.e., the hit counter increments when connected to their respective Redis instances).

**5. Cleanup:**
   ```bash
   # Stop and remove containers, networks from the dev setup
   docker-compose down

   # Stop and remove containers, networks from the prod setup
   docker-compose -f docker-compose.prod.yml down
   ```

---

## ✅ Validation Checklist

- [ ] `Dockerfile.prod` contains a `builder` stage and a `final` stage.
- [ ] The `builder` stage in `Dockerfile.prod` installs dependencies from `app/requirements.txt` into a virtual environment.
- [ ] (Optional Bonus) The `builder` stage runs `pytest` successfully.
- [ ] The `final` stage in `Dockerfile.prod` uses a slim Python base image.
- [ ] The `final` stage copies the virtual environment and necessary application code (e.g., `main.py`) from the `builder` stage.
- [ ] `docker-compose.prod.yml` correctly defines `web_prod` and `redis_prod` services.
- [ ] The `web_prod` service in `docker-compose.prod.yml` builds using `Dockerfile.prod`.
- [ ] `docker-compose -f docker-compose.prod.yml up --build -d` starts both services successfully.
- [ ] The application running from the production image is accessible and functional (e.g., at `http://localhost:5005`).
- [ ] Running `docker images` shows that the image built via `Dockerfile.prod` is significantly smaller than the image built via `app/Dockerfile` (dev version).

---

## 🧹 Further Cleanup (Optional)

-   Remove specific Docker images if desired:
    ```bash
    docker rmi <dev_image_name_or_id>
    docker rmi <prod_image_name_or_id>
    ```
-   Prune unused images (be careful with this command):
    ```bash
    docker image prune
    ```

---

## 🧠 Key Concepts Review

-   **Multi-Stage Builds**: Using multiple `FROM` statements in a Dockerfile to create intermediate build stages. Artifacts can be copied from one stage to the next, allowing final images to be minimal.
-   **Builder Pattern**: A common use of multi-stage builds where one or more stages prepare the application (compile code, install all dependencies including dev/test tools), and a final stage copies only the runtime artifacts to a lean base image.
-   `COPY --from=<stage_name_or_index>`: The Dockerfile instruction used to copy files from a previous stage.
-   **Image Optimization**: Reducing Docker image size leads to faster deployments, lower storage costs, and a reduced attack surface.
-   **Separation of Concerns**: Keeping development/build tooling separate from the runtime environment of the production image.

---

## 🔁 What's Next?

You've learned a critical technique for creating optimized Docker images suitable for production environments. 

Consider exploring **[../LAB05-Secrets-And-Volumes/README.md](../LAB05-Secrets-And-Volumes/)** next, which will delve into managing secrets and persistent data with Docker and Docker Compose. 