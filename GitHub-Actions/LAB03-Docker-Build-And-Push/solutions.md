# Solutions for LAB03 - Docker Build & Push

This file contains the solutions for the `TODO` items in the `.github/workflows/docker-publish.yml` workflow file.

---

## `docker-publish.yml` Solutions

```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/my-cicd-lab-app:latest
            ${{ secrets.DOCKER_USERNAME }}/my-cicd-lab-app:${{ github.sha }}
```

---

### Explanation (`docker-publish.yml`):

1.  **Trigger Configuration (`on`):**
    *   `on: push: branches: [ main ]`: The workflow triggers only on push events to the `main` branch.

2.  **Runner OS (`runs-on`):**
    *   `runs-on: ubuntu-latest`: The job will run on the latest Ubuntu runner provided by GitHub Actions.

3.  **Checkout Code (`uses: actions/checkout@v3`):**
    *   This step checks out the repository code so the Docker build process can access the `Dockerfile` and the `app/` directory.

4.  **Log in to Docker Hub (`uses: docker/login-action@v3`):**
    *   This step uses the official `docker/login-action` (version 3).
    *   `with: username: ${{ secrets.DOCKER_USERNAME }} password: ${{ secrets.DOCKER_PASSWORD }}`: It securely uses credentials stored as GitHub secrets (`DOCKER_USERNAME` and `DOCKER_PASSWORD`) to log in to Docker Hub. Students need to configure these secrets in their repository settings.

5.  **Build and Push Docker Image (`uses: docker/build-push-action@v5`):**
    *   This step uses the official `docker/build-push-action` (version 5).
    *   `context: .`: Sets the Docker build context to the root of the repository (where the `Dockerfile` is).
    *   `push: true`: Instructs the action to push the image to the registry after a successful build.
    *   `tags: | ...`: Specifies the tags for the Docker image. Using the pipe `|` allows for multi-line input.
        *   `${{ secrets.DOCKER_USERNAME }}/my-cicd-lab-app:latest`: Tags the image with `latest`. Replace `my-cicd-lab-app` with a preferred repository name.
        *   `${{ secrets.DOCKER_USERNAME }}/my-cicd-lab-app:${{ github.sha }}`: Tags the image with the commit SHA. This provides a unique tag for each commit, which is excellent for traceability.

### Important Notes for Students:

*   **Docker Hub Account:** You must have a Docker Hub account.
*   **GitHub Secrets:** Before this workflow can successfully push to Docker Hub, you need to configure two secrets in your GitHub repository settings (under `Settings` > `Secrets and variables` > `Actions`):
    *   `DOCKER_USERNAME`: Your Docker Hub username.
    *   `DOCKER_PASSWORD`: A Docker Hub access token is highly recommended instead of your actual password. You can generate an access token from your Docker Hub account settings (`Account Settings` > `Security` > `New Access Token`).
*   **Image Name:** In the `tags` section, `my-cicd-lab-app` is a placeholder. You should ideally use a unique name for your Docker Hub repository, e.g., `yourusername/lab03-app`. 