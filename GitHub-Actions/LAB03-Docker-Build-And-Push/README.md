# LAB03 - Docker Build & Push (GitHub Actions)

In this lab, you’ll learn how to use GitHub Actions to build a Docker image and push it to Docker Hub automatically after each commit to the `main` branch.

---

## 🎯 Objectives

By the end of this lab, you will:
- Build a Docker image using GitHub Actions
- Tag the image with commit SHA or version number
- Push the image to Docker Hub using secrets

---

## 🧰 Prerequisites

- A [Docker Hub](https://hub.docker.com) account
- A GitHub repository with a Dockerfile and Python app
- GitHub Secrets: `DOCKER_USERNAME` and `DOCKER_PASSWORD`

---

## 🗂️ Folder Structure

```bash
GitHub-Actions/LAB03-Docker-Build-And-Push/
├── .github/
│   └── workflows/
│       └── docker-publish.yml
├── app/
│   └── main.py
├── Dockerfile
└── README.md
```

---

## 🚀 Getting Started

1. **Create a basic Python app and Dockerfile:**
```python
# app/main.py
print("Dockerized app running")
```
```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app/ ./
CMD ["python", "main.py"]
```

2. **Create a GitHub Actions workflow:**
```yaml
# .github/workflows/docker-publish.yml
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
        tags: ${{ secrets.DOCKER_USERNAME }}/ci-lab-app:latest
```

3. **Push and verify image in Docker Hub.**

---

## ✅ Validation Checklist

- [ ] Image built and tagged correctly
- [ ] Credentials used from GitHub Secrets
- [ ] Image pushed to Docker Hub repository

---

## 🧹 Cleanup
- Remove Dockerfile or delete repo if this was temporary
- Revoke `DOCKER_PASSWORD` if shared temporarily

---

## 🧠 Key Concepts

- GitHub Actions can run Docker CLI and official actions
- Secrets keep your Docker credentials secure
- Tags help manage versioning and deployments

---

## 🔁 What's Next?
Continue to [LAB04 - Deploy to GitHub Pages](../LAB04-Deploy-GitHub-Pages/) to publish static sites from your CI workflows.

Push containers like a pro. 🐳🚀