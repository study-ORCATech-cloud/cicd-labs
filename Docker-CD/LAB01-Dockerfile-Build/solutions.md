# Solutions for LAB01: Your First Dockerfile for a Python Web App

This document provides the completed `Dockerfile` for LAB01 and a brief explanation of each instruction used. Students should refer to this after attempting to complete the `TODO`s in the `Dockerfile` themselves.

---

## ✅ Completed `Dockerfile`

Here is the complete and working `Dockerfile` for containerizing the simple Python Flask application:

```dockerfile
# Solution for TODO_BASE_IMAGE: Specify the base image.
# For a Python Flask application, a good choice is a Python slim image.
FROM python:3.9-slim

# Solution for TODO_WORKDIR: Set the working directory inside the container.
# This is where your application code will live and commands will be run.
WORKDIR /app

# Solution for TODO_COPY_REQUIREMENTS: Copy the requirements.txt file into the container.
# This should be done before copying the rest of the app, for Docker layer caching benefits.
COPY ./app/requirements.txt .

# Solution for TODO_INSTALL_DEPS: Install the Python dependencies.
# Use pip to install the packages listed in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Solution for TODO_COPY_APP: Copy the rest of the application code (the ./app directory) into the container's working directory.
COPY ./app/ .

# Solution for TODO_EXPOSE_PORT: Expose the port the Flask application will run on.
# Our Flask app in app/main.py is configured to run on port 5000.
EXPOSE 5000

# Solution for TODO_CMD: Specify the command to run when the container starts.
# This should execute the Flask application (main.py).
CMD ["python", "main.py"]
```

---

## 📝 Explanation of `Dockerfile` Instructions

1.  **`FROM python:3.9-slim`**
    *   This line specifies the base image for our Docker image. We're using `python:3.9-slim`, which is an official Python image that is relatively small (due to the `-slim` tag) and comes with Python 3.9 pre-installed.

2.  **`WORKDIR /app`**
    *   This sets the working directory inside the container to `/app`. All subsequent `COPY`, `RUN`, and `CMD` instructions will be executed relative to this directory.

3.  **`COPY ./app/requirements.txt .`**
    *   This copies the `requirements.txt` file from the `app` subdirectory of our build context (our current directory on the host) into the `/app` directory (the current `WORKDIR`) inside the image.
    *   Copying and installing requirements *before* copying the rest of the application code is a best practice for Docker layer caching. If your application code changes but `requirements.txt` doesn't, Docker can reuse the layer where dependencies were installed, speeding up the build.

4.  **`RUN pip install --no-cache-dir -r requirements.txt`**
    *   This command executes `pip install` inside the container to install the Python packages listed in `requirements.txt`. The `--no-cache-dir` option tells pip not to store the downloaded packages in a cache, which helps keep the image size smaller.

5.  **`COPY ./app/ .`**
    *   This copies the entire contents of the `app` subdirectory from our build context into the `/app` directory (the current `WORKDIR`) inside the image. This includes our `main.py` file.

6.  **`EXPOSE 5000`**
    *   This instruction documents that the application inside the container will listen on port `5000` at runtime. It doesn't actually publish the port; publishing is done with the `-p` flag when running `docker run`.

7.  **`CMD ["python", "main.py"]`**
    *   This specifies the default command to execute when a container is started from this image. It will run `python main.py`, which starts the Flask development server.
    *   The `CMD` instruction should be used in its "exec form" (as a JSON array) for best practices, as it avoids a shell being invoked.

---

With this `Dockerfile`, you can build a self-contained image of your Python Flask application that can be run consistently across different environments. 