# LAB05: Building Docker Images with Jenkins

In this lab, you'll configure a Jenkins pipeline to automatically build a Docker image for a Python Flask web application. You will work with a provided `Dockerfile` and complete a `Jenkinsfile` to orchestrate the build process, optionally test the image by running a container, and prepare for pushing it to a container registry.

This lab emphasizes how Jenkins integrates with Docker to automate the packaging of applications into portable container images, a cornerstone of modern CI/CD.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand how a Jenkins pipeline can build Docker images using a `Dockerfile`.
- Configure a `Jenkinsfile` with appropriate agent settings for Docker builds.
- Use Docker-specific commands within a `Jenkinsfile` (e.g., `docker.build()`).
- Define and use environment variables in your `Jenkinsfile` for image naming and tagging.
- (Optional) Add steps to run the built Docker image for basic testing.
- (Optional) Understand the steps required to push an image to a Docker registry like Docker Hub.

---

## 🧰 Prerequisites

-   **Jenkins Installed and Running:** Jenkins must be installed and accessible. Refer to **`../../install-and-setup.md`**.
    *   **Docker Integration with Jenkins:** Your Jenkins environment (controller or a designated agent) must have Docker installed and configured so that Jenkins can execute Docker commands.
        *   If Jenkins itself is running in a Docker container (as per the setup guide), ensure the Docker socket (`/var/run/docker.sock`) is mounted into the Jenkins container, and the `docker` CLI is available within it or that you use a Docker agent in your pipeline.
        *   The Jenkins user (or the user the Jenkins agent runs as) needs permission to access the Docker daemon.
-   **Docker Hub Account (Optional):** If you want to complete the optional "Push Docker Image" stage, you'll need a Docker Hub account.
-   **Jenkins Credentials for Docker Hub (Optional):** If pushing to Docker Hub, you'll need to configure your Docker Hub credentials in Jenkins (`Manage Jenkins` -> `Credentials`). A credential ID will be needed in the `Jenkinsfile`.
-   **GitHub Account and Fork:** Your forked `cicd-labs` repository. You will be working with the files in `Jenkins/LAB05-Docker-Image-Build/`.

---

## 📂 Folder Structure for This Lab

```bash
Jenkins/LAB05-Docker-Image-Build/
├── README.md         # Lab overview, objectives, prerequisites, TODO explanations (this file)
├── Jenkinsfile       # The Declarative Pipeline script you will complete (with TODOs)
├── solutions.md      # Contains the completed Jenkinsfile
└── app/
    ├── main.py           # Simple Python Flask web application (provided)
    ├── requirements.txt  # Python dependencies for the Flask app (provided)
    └── Dockerfile        # Dockerfile to containerize the Flask app (provided, complete)
```

---

## 🐍 Understanding the Sample Application

The `app/` directory contains:
-   `main.py`: A very simple web server built with [Flask](https://flask.palletsprojects.com/). It serves a greeting message at the root (`/`) URL.
-   `requirements.txt`: Specifies `Flask` as a dependency.
-   `Dockerfile`: A complete, standard Dockerfile that:
    1.  Starts from a `python:3.9-slim` base image.
    2.  Sets `/app` as the working directory.
    3.  Copies `requirements.txt` and installs dependencies using `pip`.
    4.  Copies `main.py` into the image.
    5.  Exposes port `5000` (which Flask uses by default for development).
    6.  Sets environment variables for Flask.
    7.  Specifies `flask run` as the command to start the application.

Your task is **not** to modify these application files or the `Dockerfile`, but to create a Jenkins pipeline that can build an image from this `Dockerfile`.

---

## 🚀 Lab Steps: Completing Your `Jenkinsfile`

Your primary task is to complete the `Jenkins/LAB05-Docker-Image-Build/Jenkinsfile`. This file has `TODO:` markers indicating where you need to add or modify Groovy code.

**1. Locate and Open `Jenkinsfile`:**
   Open `Jenkins/LAB05-Docker-Image-Build/Jenkinsfile` in your local clone of your forked repository.

**2. Complete the `TODO` items in `Jenkinsfile`:**

   *   **`TODO_AGENT_SETUP` (Lines 2-18):**
        *   **Goal:** Configure an agent that can execute Docker commands.
        *   **Considerations:**
            *   If your main Jenkins instance (or a pre-configured agent) has Docker installed and accessible, `agent any` *might* work.
            *   A more robust method is to use a Docker agent (e.g., `agent { docker { image 'docker:24.0-git' ... } }`). This ensures the Docker CLI is available. If you choose this, ensure the Docker socket is mounted (`args '-v /var/run/docker.sock:/var/run/docker.sock ...'`) so the containerized agent can interact with the host's Docker daemon to build images.
            *   Refer to the comments in the `Jenkinsfile` for specific examples and choose/adapt one for your Jenkins setup. The provided default in the skeleton uses a Docker agent.

   *   **`TODO_IMAGE_NAME` (Line 22):**
        *   **Goal:** Define a name for your Docker image.
        *   **Action:** Set the `IMAGE_NAME` environment variable.
        *   For local testing, a simple name like `'lab05-flask-app'` is fine.
        *   If you plan to push to Docker Hub, use `'your-dockerhub-username/lab05-flask-app'`. **Replace `your-dockerhub-username` with your actual Docker Hub username.** If you don't have one or don't want to push, use a local-only name.

   *   **`TODO_IMAGE_TAG` (Line 25, already partially complete):**
        *   **Goal:** Define a tag for your Docker image. Using `env.BUILD_NUMBER` makes tags unique per build.
        *   **Action:** This is mostly complete (`"0.1.${env.BUILD_NUMBER}"`). Review its purpose.

   *   **`TODO_BUILD_IMAGE` (Lines 40-49):**
        *   **Goal:** Add the command to build your Docker image.
        *   **Action:** Inside the `script` block, use the `docker.build()` command.
        *   You'll need to provide the image name (e.g., `"${IMAGE_NAME}:${IMAGE_TAG}"`) and the path to the Dockerfile context. The path to the directory containing the `Dockerfile` is stored in the `DOCKERFILE_PATH` environment variable.
        *   Example: `docker.build("${IMAGE_NAME}:${IMAGE_TAG}", "--pull -f ${DOCKERFILE_PATH}/Dockerfile ${DOCKERFILE_PATH}")`
            *   The `--pull` argument ensures the base image is up-to-date.
            *   The first argument to `docker.build()` is the full image name and tag.
            *   The second argument provides additional flags for the `docker build` command, like `-f` to specify the Dockerfile location and the final argument is the build context path.

   *   **`TODO_RUN_IMAGE` (Optional) (Lines 62-75):**
        *   **Goal:** (Optional) Add shell commands to run the newly built image as a container to test it.
        *   **Action:** In the `sh ''` placeholder:
            *   Use `docker run` to start your container.
            *   Run it in detached mode (`-d`).
            *   Map the container's port `5000` to a host port (e.g., `-p 5001:5000`).
            *   Give the container a name for easy reference (e.g., `--name lab05app`).
            *   Use `--rm` so the container is removed when stopped.
            *   Example: `sh 'docker run -d -p 5001:5000 --name lab05app --rm ${IMAGE_NAME}:${IMAGE_TAG}'`
        *   **Further steps (in the `script` block, optional):**
            *   Add a `sleep 10` to give the app time to start.
            *   Use `sh 'curl http://localhost:5001'` to check if the app responds.
            *   Use `sh 'docker logs lab05app'` to view container logs.
            *   Use `sh 'docker stop lab05app'` to stop the container (it will be auto-removed due to `--rm`).

   *   **`TODO_PUSH_IMAGE` (Optional/Advanced) (Lines 86-101):**
        *   **Goal:** (Optional) Add commands to push your image to a container registry (e.g., Docker Hub).
        *   **Prerequisites:**
            *   You must have set `IMAGE_NAME` to your full Docker Hub repository name (e.g., `yourusername/lab05-flask-app`).
            *   You must have configured your Docker Hub credentials in Jenkins (`Manage Jenkins` -> `Credentials`) and know the **Credential ID**.
        *   **Action:** Inside the `script` block:
            *   Use `docker.withRegistry('', 'your-jenkins-docker-credential-id') { ... }`. Replace `your-jenkins-docker-credential-id` with your actual Jenkins credential ID. The first empty string `''` signifies Docker Hub as the registry.
            *   Inside the block, use `docker.image("${IMAGE_NAME}:${IMAGE_TAG}").push()`.
            *   You can also optionally push a `latest` tag: `docker.image("${IMAGE_NAME}").push('latest')`.
        *   This entire stage is optional and can be skipped if you don't want to push to a registry.

   *   **`TODO_CLEANUP_RUNNING_CONTAINER` (Optional) (Lines 136-139):**
        *   **Goal:** (Optional) Ensure any test container is stopped and removed.
        *   **Action:** This is mainly a fallback if the `docker run` command in the test stage didn't use `--rm` or if you need more explicit cleanup. The provided comments show `sh 'docker stop lab05app || true'` and `sh 'docker rm lab05app || true'`. The `|| true` prevents the pipeline from failing if the container doesn't exist.

**3. Commit and Push `Jenkinsfile` Changes:**
   Once you have completed the relevant `TODO`s, commit the modified `Jenkinsfile` to your forked GitHub repository and push the changes.

**4. Configure and Run Jenkins Pipeline Job:**
   *   In Jenkins, create a new "Pipeline" job (e.g., `docker-build-pipeline`).
   *   Configure it to use "Pipeline script from SCM," pointing to your forked repository and the `Jenkins/LAB05-Docker-Image-Build/Jenkinsfile` script path.
   *   Ensure the branch is correct (e.g., `*/main`).
   *   Save and click "Build Now."

---

## ✅ Validation Checklist

- [ ] The `Jenkinsfile` has been completed with appropriate agent setup, image name, and build commands.
- [ ] The Jenkins pipeline job runs successfully.
- [ ] The "Build Docker Image" stage completes, and logs indicate a successful `docker build`.
- [ ] (If `TODO_RUN_IMAGE` is completed) The "Test Run Docker Image" stage:
    - [ ] Successfully starts the container.
    - [ ] `curl` command (if added) retrieves the "Hello from your Flask app..." message.
    - [ ] Container is stopped and removed.
- [ ] (If `TODO_PUSH_IMAGE` is completed and credentials configured) The image is pushed to your Docker Hub repository. You can verify this by logging into Docker Hub.
- [ ] Check Jenkins console output for any errors or success messages.

---

## 🧹 Cleanup

1.  **Jenkins Job:** Delete the `docker-build-pipeline` job in Jenkins if no longer needed.
2.  **Docker Images:** On the Jenkins agent/machine where the Docker images were built:
    *   List images: `docker images`
    *   Remove the specific image: `docker rmi your-image-name:tag` (e.g., `docker rmi lab05-flask-app:0.1.1` or `docker rmi yourusername/lab05-flask-app:0.1.1`)
    *   To remove all unused images (use with caution): `docker image prune -a -f`
3.  **Docker Containers (if any left running):**
    *   List running containers: `docker ps`
    *   List all containers: `docker ps -a`
    *   Stop a container: `docker stop container_name_or_id`
    *   Remove a container: `docker rm container_name_or_id`
4.  **Docker Hub (if pushed):** You can delete the test image/repository from your Docker Hub account if desired.

---

## 🧠 Key Concepts

-   **Dockerfile:** A text document that contains all the commands a user could call on the command line to assemble an image. Jenkins uses this file to build your image.
-   **Docker Image:** A lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries, and settings.
-   **Docker Container:** A runtime instance of a Docker image.
-   **Jenkins Agent for Docker:** The Jenkins pipeline needs to run on an agent (or the controller itself) that has Docker installed and configured correctly for the Jenkins user. Alternatively, a Docker container can serve as the agent.
-   **`docker.build("image_name:tag", "path_to_context")`:** A Jenkins Pipeline step (from the Docker Pipeline plugin) to build a Docker image.
    *   The second argument can include flags like `--pull -f path/to/Dockerfile`.
-   **`docker.withRegistry('registry_url', 'credentials_id') { ... }`:** A Jenkins Pipeline step to interact with a Docker registry (like Docker Hub). Requires credentials to be set up in Jenkins.
-   **Image Tagging:** Assigning a version or label to your Docker image (e.g., `myapp:1.0`, `myapp:latest`). Using `env.BUILD_NUMBER` helps create unique tags for each build.
-   **Docker Socket Mounting (`-v /var/run/docker.sock:/var/run/docker.sock`):** When running Docker-in-Docker or using a Dockerized Jenkins agent to build images on the host, this allows the container to communicate with the host's Docker daemon.

---

## 🔁 What's Next?

After building and managing Docker images, you'll explore more advanced pipeline syntax for parallel execution and conditional logic.

Proceed to **[../LAB06-Parallel-And-Conditional/README.md](../LAB06-Parallel-And-Conditional/)**.

Containerize with confidence. 🐳⚙️🚀

