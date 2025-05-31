# LAB03 - Docker Build & Push (GitHub Actions)

In this lab, you'll learn how to use GitHub Actions to build a Docker image from a `Dockerfile` and a simple Python application, and then push it to Docker Hub automatically after each commit to the `main` branch. This is a cornerstone of modern CI/CD for containerized applications.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand how to use the `docker/login-action` to securely log in to Docker Hub using GitHub Secrets.
- Configure the `docker/build-push-action` to build a Docker image from a `Dockerfile` within your repository.
- Tag Docker images effectively using both static tags (like `latest`) and dynamic tags (like commit SHA).
- Push the built Docker image to a Docker Hub repository.
- Set up a GitHub Actions workflow that triggers on pushes to the `main` branch.

---

## 🧰 Prerequisites

- A [Docker Hub](https://hub.docker.com/) account. (Create one if you haven't already.)
- A GitHub repository where you can implement this lab.
- **Crucially**: You must configure the following secrets in your GitHub repository settings (under `Settings` > `Secrets and variables` > `Actions`):
    - `DOCKER_USERNAME`: Your Docker Hub username.
    - `DOCKER_PASSWORD`: **Use a Docker Hub Access Token here, not your actual password.** You can generate an access token from your Docker Hub account settings (`Account Settings` > `Security` > `New Access Token`). This is much more secure.

---

## 🗂️ Folder Structure

Your lab directory is already set up with the following structure. You will be working primarily with the `docker-publish.yml` file.

```bash
GitHub-Actions/LAB03-Docker-Build-And-Push/
├── .github/
│   └── workflows/
│       └── docker-publish.yml  # Your partially completed workflow file with TODOs
├── app/
│   └── main.py               # A simple Python application (provided)
├── Dockerfile               # Dockerfile for the Python app (provided)
├── README.md                # Lab instructions (this file)
└── solutions.md             # Solutions for docker-publish.yml
```

---

## 🚀 Lab Steps

1.  **Navigate to the Lab Directory:**
    Open your terminal and change to the `GitHub-Actions/LAB03-Docker-Build-And-Push/` directory.

2.  **Examine the Python Application (`app/main.py`):**
    Open `app/main.py`. This is a very simple Python script that prints a message. It's provided for you to have something to Dockerize.

3.  **Examine the Dockerfile (`Dockerfile`):**
    Open `Dockerfile`. This file contains the instructions to build a Docker image for the Python application. Review its contents to understand how the image is constructed (base image, working directory, copying files, run command).

4.  **Set Up GitHub Secrets (CRITICAL STEP):**
    *   Go to your GitHub repository settings.
    *   Navigate to `Secrets and variables` > `Actions`.
    *   Click `New repository secret`.
    *   Create `DOCKER_USERNAME` with your Docker Hub username as the value.
    *   Create `DOCKER_PASSWORD` with your Docker Hub **Access Token** as the value.
    *   **Your workflow will fail if these secrets are not correctly configured.**

5.  **Complete the GitHub Actions Workflow (`.github/workflows/docker-publish.yml`):**
    Open `.github/workflows/docker-publish.yml`. This file contains a partially completed workflow with `TODO` comments.
    Your tasks are to complete the `TODO` sections in this YAML file:
    *   Configure the `on` trigger for pushes to the `main` branch.
    *   Set the `runs-on` key for the job (e.g., `ubuntu-latest`).
    *   Use `actions/checkout@v3` to checkout code.
    *   Use `docker/login-action@v3` to log in to Docker Hub using your configured `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets.
    *   Use `docker/build-push-action@v5` to build and push the image.
        *   Set `context: .`
        *   Set `push: true`
        *   Define `tags`. Use at least two tags: one static (e.g., `your-dockerhub-username/your-app-name:latest`) and one dynamic using the commit SHA (e.g., `your-dockerhub-username/your-app-name:${{ github.sha }}`). **Remember to replace `your-dockerhub-username` and `your-app-name` with your actual Docker Hub username and a chosen application name.**
    Refer to the hints in the `TODO` comments.

6.  **Commit and Push Your Changes:**
    Once you have completed all the `TODO`s in `.github/workflows/docker-publish.yml`:
    ```bash
    git add .github/workflows/docker-publish.yml
    git commit -m "feat: Implement Docker build and push workflow for LAB03"
    git push origin main
    ```

7.  **Verify Workflow Execution and Docker Hub Image:**
    *   Go to your GitHub repository and open the "Actions" tab. You should see your "Docker Build and Push" workflow running or completed.
    *   Inspect the logs for the `build-and-push` job. Verify that all steps, including login, build, and push, completed successfully.
    *   Log in to your [Docker Hub](https://hub.docker.com/) account.
    *   Navigate to your repositories. You should see a new repository (e.g., `your-app-name` or whatever you chose) with the tags `latest` and one matching the commit SHA from your push.

---

## ✅ Validation Checklist

- [ ] GitHub secrets `DOCKER_USERNAME` and `DOCKER_PASSWORD` (Access Token) are correctly configured in the repository.
- [ ] The `.github/workflows/docker-publish.yml` file is correctly completed.
- [ ] Pushing changes to `main` triggers the "Docker Build and Push" workflow.
- [ ] The workflow successfully logs in to Docker Hub.
- [ ] The Docker image is built successfully.
- [ ] The Docker image is tagged with both `latest` and the commit SHA.
- [ ] The Docker image is pushed to your Docker Hub repository and is visible there with the correct tags.
- [ ] You understand where to find the `solutions.md` file for this lab.

---

## 💡 Solutions

If you get stuck or want to verify your work, refer to the `solutions.md` file provided in this lab directory. It contains the complete working code for `docker-publish.yml` with explanations.

---

## 🧹 Cleanup

-   **From Docker Hub:** You can delete the repository or specific tags from your Docker Hub account if desired.
-   **From GitHub:**
    ```bash
    rm .github/workflows/docker-publish.yml
    # The app/main.py and Dockerfile can be kept or removed as per your preference.
    # rm -rf app/
    # rm Dockerfile
    ```
    Commit and push the deletions.
-   **GitHub Secrets:** Consider removing or revoking the `DOCKER_PASSWORD` (Access Token) from your GitHub repository secrets if it was created solely for this lab and is no longer needed, especially if it had broad permissions.

---

## 🧠 Key Concepts

-   **`docker/login-action`:** A GitHub Action for securely logging into a Docker registry (like Docker Hub).
-   **`docker/build-push-action`:** A GitHub Action for building Docker images and pushing them to a registry.
-   **GitHub Secrets:** Encrypted environment variables for storing sensitive information like passwords or access tokens, accessible within workflows.
-   **Dockerfile:** A text document that contains all the commands a user could call on the command line to assemble an image.
-   **Image Tagging:** Assigning labels (tags) to Docker images, often used for versioning (e.g., `v1.0.0`, `latest`, commit SHA).
-   **Docker Hub:** A cloud-based registry service for finding and sharing Docker images.

---

## 🌟 Well Done!

You've now automated the process of building and publishing Docker images using GitHub Actions. This is a fundamental skill for containerized application delivery!

---

## 🔁 What's Next?
Continue to [LAB04 - Deploy to GitHub Pages](../LAB04-Deploy-GitHub-Pages/) to publish static sites from your CI workflows.

Push containers like a pro. 🐳🚀