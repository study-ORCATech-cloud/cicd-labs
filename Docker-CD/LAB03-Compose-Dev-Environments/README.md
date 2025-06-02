# LAB03: Efficient Local Development with Docker Compose Volumes and Environment Variables

This lab focuses on optimizing your local development workflow using Docker Compose. You will learn how to use **volumes** to mount your local source code directly into your running containers, enabling **live reloading** of your application when you make changes. Additionally, you'll use **environment variables** within Docker Compose to configure your application for a development environment (e.g., enabling debug mode).

We will continue using the Python Flask web application with a Redis hit counter from Lab 02.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand and implement Docker volumes to map local source code into a container for live updates.
- Configure development-specific settings (like Flask's debug mode) using environment variables in `docker-compose.yml`.
- Experience a faster development cycle by making code changes locally and seeing them reflected in the container without rebuilding the Docker image.
- Run and manage the multi-container application (web app + Redis) in a development-friendly setup.

---

## 🧰 Prerequisites

-   **Completion of Docker-CD Lab 02:** Understanding of basic `docker-compose.yml` structure and commands (`up`, `down`, `ps`, `run`).
-   **Docker and Docker Compose Installed.**
-   **Basic Terminal/Command Line Knowledge.**
-   **Text Editor/IDE.**
-   Familiarity with file paths.

---

## 📂 Folder Structure for This Lab

```bash
Docker-CD/LAB03-Compose-Dev-Environments/
├── app/                            # Python Flask application with Redis (copied from Lab02)
│   ├── Dockerfile                  # Dockerfile for the web app (COMPLETE)
│   ├── main.py                     # Flask app logic with Redis counter (COMPLETE, minor dev mode text changes)
│   ├── requirements.txt            # Python dependencies (COMPLETE)
│   └── tests/
│       └── test_main.py            # Basic unit tests (COMPLETE)
├── docker-compose.yml              # Docker Compose definition for development (contains TODOs)
├── README.md                       # Lab instructions (this file)
└── solutions.md                    # Completed docker-compose.yml
```

--- 

## 🐍 The Sample Application (`app/`)

The `app/` directory contains the same Python Flask and Redis hit-counter application as in Lab 02. The `main.py` file has been slightly modified to indicate "(Dev Mode)" in its output messages, and its `app.run()` call is simplified as Flask's debug mode and reloader are typically activated via environment variables.

**You do NOT need to modify the code in the `app/` directory. It is provided as a complete example.** Your focus is on configuring `docker-compose.yml` for an efficient development experience.

---

## 🐳 Configuring Docker Compose for Development

Your primary task is to modify the `docker-compose.yml` file to enable a smooth local development workflow.

**Key Concepts for Development Environments:**

*   **Volumes for Live Reloading:**
    Docker volumes can map a directory from your host machine (where your source code resides) to a directory inside your container. When you edit files on your host, these changes are instantly available within the container. If your application server (like Flask in debug mode) watches for file changes, it can automatically reload, allowing you to see your updates in near real-time without rebuilding the Docker image.

*   **Environment Variables for Configuration:**
    Applications often behave differently in development versus production. Environment variables are a great way to control these settings. For example, you can set `FLASK_ENV=development` or `FLASK_DEBUG=1` to enable Flask's built-in debugger and auto-reloader.

**1. Examine the `docker-compose.yml` file:**

   Open `docker-compose.yml`. It's pre-filled with a basic structure for the `web` and `redis` services, similar to Lab 02, but with new `TODO`s related to development settings.

**2. Complete the `TODO` items in `docker-compose.yml`:**

   *   **`web` service:**
        *   **`TODO_VOLUMES_DEV`**: This is the crucial step for live reloading.
            *   **Action**: Configure the `volumes` section for the `web` service to mount your local `./app` directory (relative to the `docker-compose.yml` file) to the `/usr/src/app` directory inside the container (which is the `WORKDIR` defined in the `app/Dockerfile`).
            *   **Syntax hint**: `volumes: - ./your-local-app-path:/path/inside/container`

        *   **`TODO_ENVIRONMENT_DEV`**: Set environment variables to enable development mode for Flask.
            *   **Action**: In the `environment` section for the `web` service:
                1.  Ensure `REDIS_HOST=redis` is still present (or add it if missing) so the app can find the Redis service.
                2.  Add an environment variable to enable Flask's development mode. You can use **either** `FLASK_ENV=development` **or** `FLASK_DEBUG=1`. Both will typically enable the debugger and reloader for Flask. The `app/main.py` is set up to respond to these.
            *   **Syntax hint**: `environment: - VARIABLE_NAME=value` or a list of `VARIABLE_NAME: value` pairs.

**3. Test Your Development Environment:**

   Navigate to `Docker-CD/LAB03-Compose-Dev-Environments/` in your terminal.

   *   **Build (if first time or Dockerfile changed) and run services:**
        ```bash
        docker-compose up --build
        ```
        *   `--build`: Ensures images are built, especially if it's the first run or if `app/Dockerfile` changed (though it shouldn't for this lab).
        *   Notice we are *not* using `-d` (detached mode) initially. This way, you can see the application logs directly in your terminal, which is often helpful during development to see reloads and debug messages.

   *   **Access the web app:** Open your browser to `http://localhost:5003` (note the port `5003` specified in this lab's `docker-compose.yml` to avoid conflicts if Lab02 is also running).
        You should see the hit counter app, with "(Dev Mode)" in the messages.

   *   **Test live reloading:**
        1.  Keep `docker-compose up` running in your terminal.
        2.  Open `app/main.py` in your text editor.
        3.  Find the main greeting string in the `hello_world()` function (e.g., `f'Hello from the Web App! ... (Dev Mode)\n'`).
        4.  Change this string to something new (e.g., add your name or a different message).
        5.  Save the `app/main.py` file.
        6.  Observe the terminal where `docker-compose up` is running. If Flask's reloader is active (due to the environment variables you set), you should see log messages indicating it detected a change and is reloading the server.
        7.  Refresh your browser page for `http://localhost:5003`. You should see your updated message immediately!

   *   **View logs (if running detached or in another terminal):**
        If you later run with `docker-compose up -d`, you can view logs using:
        ```bash
        docker-compose logs -f web
        ```
        (`-f` follows the log output)

   *   **Run unit tests (still a good practice):**
        Open another terminal, navigate to the lab directory, and run:
        ```bash
        docker-compose run --rm web pytest tests/
        ```

   *   **Stop services:**
        In the terminal where `docker-compose up` is running, press `Ctrl+C`. Then, or if it was detached, run:
        ```bash
        docker-compose down
        ```
        This command also removes the network created by Compose for this project by default.

---

## ✅ Validation Checklist

- [ ] `docker-compose.yml` correctly defines the `web` and `redis` services.
- [ ] The `web` service in `docker-compose.yml` has a volume mount correctly mapping `./app` to `/usr/src/app`.
- [ ] The `web` service in `docker-compose.yml` has environment variables set for `REDIS_HOST` and Flask development/debug mode (e.g., `FLASK_ENV=development` or `FLASK_DEBUG=1`).
- [ ] `docker-compose up --build` successfully starts both services.
- [ ] The Flask application (web service) shows "(Dev Mode)" in its output and is accessible at `http://localhost:5003`.
- [ ] Modifying `app/main.py` on the host machine and saving the file causes the Flask server (running in the container) to automatically reload (check terminal logs from `docker-compose up`).
- [ ] The changes made to `app/main.py` are reflected in the browser upon refreshing, without needing to run `docker-compose build` or restart the containers manually.
- [ ] `docker-compose run --rm web pytest tests/` executes successfully.
- [ ] `docker-compose down` stops and removes the containers.

---

## 🧹 Cleanup

**Local:**
- If services are running locally, run: `docker-compose down`
- If you used named volumes for Redis data (optional in this lab) and want to remove them, use `docker-compose down -v`.
- To remove images built for this lab (optional): `docker image rm <image_name_or_id_for_web_service>`

---

## 🧠 Key Concepts Review

-   **Docker Volumes for Development**: Mapping a host directory to a container directory (e.g., `./app:/usr/src/app`) is a common pattern for development. It allows the application inside the container to access and use the source code files directly from the host. Changes on the host are seen instantly by the container.
-   **Live Reloading / Hot Reloading**: When combined with a development server that watches for file changes (like Flask in debug mode), volume mapping enables live reloading. The server detects changes in the mounted volume and automatically restarts or reloads the application.
-   **`FLASK_ENV=development` / `FLASK_DEBUG=1`**: Standard Flask environment variables that enable useful development features:
    *   **Debugger**: Provides detailed error pages in the browser.
    *   **Auto-reloader**: Monitors Python files for changes and restarts the server automatically.
-   **Development Workflow with Compose**: `docker-compose up` starts your environment. You code on your host. Changes are live. `Ctrl+C` and `docker-compose down` stops it.
-   **Port Mapping**: Essential for accessing the application running inside the container from your host's browser (e.g., `"5003:5000"`).

---

## 🔁 What's Next?

You've now experienced how Docker Compose can significantly improve your local development workflow by providing live reloading and easy configuration.

Proceed to **[../LAB04-Deploy-With-GitHub-Actions/README.md](../LAB04-Deploy-With-GitHub-Actions/)** (Note: This lab was previously part of Lab02. If following the revised track focused on local Docker, this lab might be about a different Docker topic like multi-stage builds or health checks instead of GitHub Actions. Please refer to the updated ROADMAP.md).