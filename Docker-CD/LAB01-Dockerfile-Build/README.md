# LAB01: Your First Dockerfile for a Python Web App

Welcome to the first lab in the Docker-CD track! In this lab, you'll learn the fundamentals of Docker by writing a `Dockerfile` to containerize a simple Python Flask web application. This is the first crucial step towards building and deploying containerized applications in a CI/CD pipeline.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand the basic structure and common instructions of a `Dockerfile` (`FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`).
- Write a `Dockerfile` from scratch to containerize a Python Flask application.
- Build a Docker image from your `Dockerfile` using `docker build`.
- Tag your Docker image for easier reference.
- Run a Docker container from your built image using `docker run`.
- Access the web application running inside the container from your local machine.
- Inspect the list of Docker images on your system.

---

## 🧰 Prerequisites

-   **Docker Installed and Running:** Docker Desktop (for Windows/Mac) or Docker Engine (for Linux) must be installed and the Docker daemon running. You can verify this by running `docker --version` and `docker ps` in your terminal.
-   **Basic Command Line Knowledge:** Familiarity with navigating directories and running commands in a terminal (Command Prompt, PowerShell, Bash, etc.).
-   **Text Editor:** Any text editor to create and edit the `Dockerfile` and Python files (e.g., VS Code, Sublime Text, Notepad++).

---

## 📂 Folder Structure for This Lab

```bash
Docker-CD/LAB01-Dockerfile-Build/
├── README.md       # Lab overview, objectives, setup, TODOs (this file)
├── Dockerfile      # Your Docker image definition (you will complete the TODOs here)
├── solutions.md    # Contains the completed Dockerfile and explanations
└── app/
    ├── main.py     # A simple Python Flask web application (provided)
    └── requirements.txt # Python dependencies for the Flask app (provided)
```

--- 

## 🐍 The Sample Python Flask Application

Located in the `app/` directory:

-   **`app/main.py`**: This is a very simple web server using Flask. It listens on port 5000 and responds with "Hello, Docker World! This is Lab 01." when you access its root URL (`/`).
-   **`app/requirements.txt`**: This file lists the Python packages needed for the application (just `Flask` in this case).

You do **not** need to modify the Python application code for this lab. Your focus will be on creating the `Dockerfile`.

---

## 🐳 Lab Steps: Creating Your `Dockerfile`

Your primary task is to complete the `Dockerfile` located in the `Docker-CD/LAB01-Dockerfile-Build/` directory. Open this file in your text editor. It contains several `TODO` comments guiding you on what Docker instructions to add.

**1. Understanding `Dockerfile` Instructions:**

A `Dockerfile` is a text document that contains all the commands a user could call on the command line to assemble an image. Here are the ones you'll use:

*   `FROM <image>:<tag>`: Specifies the base image to start from (e.g., an official Python image).
*   `WORKDIR /path/to/workdir`: Sets the working directory for subsequent instructions (`COPY`, `RUN`, `CMD`, `ENTRYPOINT`).
*   `COPY <src> <dest>`: Copies files or directories from your host machine (the build context) into the image's filesystem.
*   `RUN <command>`: Executes a command in a new layer on top of the current image and commits the results. Used for installing packages, etc.
*   `EXPOSE <port>`: Informs Docker that the container listens on the specified network ports at runtime. This is documentation; it doesn't actually publish the port.
*   `CMD ["executable","param1","param2"]`: Provides defaults for an executing container. There can only be one `CMD` instruction in a `Dockerfile`. If you list more than one `CMD` then only the last `CMD` will take effect.

**2. Complete the `TODO` items in `Dockerfile`:**

   Refer to the comments in the `Dockerfile`. Each `TODO` explains what instruction is needed and often provides an example.

   *   **`TODO_BASE_IMAGE`**: Choose an appropriate Python base image (e.g., `python:3.9-slim`).
   *   **`TODO_WORKDIR`**: Set a working directory (e.g., `/app`).
   *   **`TODO_COPY_REQUIREMENTS`**: Copy `app/requirements.txt` to your working directory in the image.
   *   **`TODO_INSTALL_DEPS`**: Use `RUN pip install` to install dependencies from `requirements.txt`.
   *   **`TODO_COPY_APP`**: Copy the entire `app/` directory into the working directory in the image.
   *   **`TODO_EXPOSE_PORT`**: Expose port `5000` (as our Flask app runs on this port).
   *   **`TODO_CMD`**: Set the default command to run the Flask app (e.g., `python main.py`).

**3. Build Your Docker Image:**

   Once you've completed the `Dockerfile`, open your terminal, navigate to the `Docker-CD/LAB01-Dockerfile-Build/` directory (where your `Dockerfile` is located), and run the build command:

   ```bash
   docker build -t my-first-flask-app:v1.0 .
   ```
   *   `docker build`: The command to build an image from a Dockerfile.
   *   `-t my-first-flask-app:v1.0`: Tags the image with a name (`my-first-flask-app`) and a tag (`v1.0`). This makes it easier to reference later.
   *   `.`: Specifies the build context (the current directory), which includes the `Dockerfile` and the `app/` directory.

   If the build is successful, you'll see output detailing the steps and a final message like "Successfully tagged my-first-flask-app:v1.0".

**4. Run a Container from Your Image:**

   Now that you have an image, you can run a container from it:

   ```bash
   docker run -d -p 5001:5000 --name flask_lab01 my-first-flask-app:v1.0
   ```
   *   `docker run`: The command to run a new container from an image.
   *   `-d`: Runs the container in detached mode (in the background).
   *   `-p 5001:5000`: Publishes the container's port `5000` (where Flask is running) to port `5001` on your host machine. This means you can access the app on `localhost:5001`.
   *   `--name flask_lab01`: Assigns a name to your running container for easier management.
   *   `my-first-flask-app:v1.0`: The name and tag of the image to run.

**5. Access Your Application:**

   Open your web browser and navigate to `http://localhost:5001`. You should see the message: "Hello, Docker World! This is Lab 01."

**6. Inspect Your Image and Container:**

   *   To see your newly built image: `docker images` (look for `my-first-flask-app`).
   *   To see your running container: `docker ps` (look for `flask_lab01`).
   *   To see container logs (if you didn't run in detached mode, or to check for errors): `docker logs flask_lab01`

---

## ✅ Validation Checklist

- [ ] All `TODO`s in `Dockerfile` are completed correctly.
- [ ] The `docker build -t my-first-flask-app:v1.0 .` command completes successfully.
- [ ] The `my-first-flask-app` image (tag `v1.0`) appears in the output of `docker images`.
- [ ] The `docker run -d -p 5001:5000 --name flask_lab01 my-first-flask-app:v1.0` command starts a container successfully.
- [ ] The `flask_lab01` container appears in the output of `docker ps`.
- [ ] Navigating to `http://localhost:5001` in a web browser displays "Hello, Docker World! This is Lab 01."

---

## 🧹 Cleanup

To stop and remove the container, and then remove the image:

1.  **Stop the container:**
    ```bash
    docker stop flask_lab01
    ```
2.  **Remove the container:** (You can only remove a stopped container unless you force it)
    ```bash
    docker rm flask_lab01
    ```
    *Alternatively, to stop and remove in one go if it's running: `docker rm -f flask_lab01`*

3.  **Remove the Docker image:**
    ```bash
    docker image rm my-first-flask-app:v1.0
    ```

--- 

## 🧠 Key Concepts Review

-   **`Dockerfile`**: A script containing instructions to assemble a Docker image.
-   **Image Layers**: Each instruction in a `Dockerfile` creates a new layer in the image. Docker caches these layers to speed up subsequent builds.
-   **Build Context**: The set of files at the specified `PATH` or `URL` (usually `.` for the current directory) sent to the Docker daemon during the build.
-   **Image Tagging (`-t name:tag`)**: Assigning a human-readable name and version to an image.
-   **Container**: A runnable instance of an image.
-   **Port Mapping (`-p hostPort:containerPort`)**: Making a container's internal port accessible on the host machine's network.
-   **Detached Mode (`-d`)**: Running a container in the background.

---

## 🔁 What's Next?

Congratulations on building your first Docker image from a `Dockerfile`!

Proceed to **[../LAB02-Compose-CI-Integration/README.md](../LAB02-Compose-CI-Integration/)** to learn about Docker Compose for managing multi-container applications.

