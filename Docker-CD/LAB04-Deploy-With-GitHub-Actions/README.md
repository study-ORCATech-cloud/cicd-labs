# LAB04 - Deploy with GitHub Actions (Docker Compose)

In this lab, you’ll automate deployment of a Docker Compose-based application using **GitHub Actions**. This is useful for deploying containerized apps to test or dev environments directly from CI.

---

## 🎯 Objectives

By the end of this lab, you will:
- Define a GitHub Actions workflow to build and deploy Compose services
- Automatically deploy on push to `main`
- Use `docker-compose` from GitHub runner

---

## 🧰 Prerequisites

- Docker installed on target server (or GitHub runner with Docker access)
- GitHub repo with:
  - `docker-compose.yml`
  - `Dockerfile`
  - App code (e.g. Flask)

---

## 🗂️ Folder Structure

```bash
Docker-CD/LAB04-Deploy-With-GitHub-Actions/
├── .github/
│   └── workflows/
│       └── deploy-compose.yml
├── app/
│   └── main.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 GitHub Actions Workflow Example
```yaml
name: Deploy Compose App

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Docker
        uses: docker/setup-buildx-action@v3

      - name: Build and Deploy with Compose
        run: |
          docker-compose -f docker-compose.yml up --build -d
```

> Note: This assumes a self-hosted runner or server with Docker access. Use `rsync` or SSH for actual deployment to remote hosts.

---

## ✅ Validation Checklist

- [ ] Workflow runs on `main` branch push
- [ ] Compose builds and starts the container
- [ ] Logs confirm service is live

---

## 🧹 Cleanup
```bash
docker-compose down
```
Remove `.github/workflows/deploy-compose.yml` if needed.

---

## 🧠 Key Concepts

- GitHub Actions automates container deployment
- `docker-compose` can run directly in CI (self-hosted)
- `up --build -d` builds and runs in the background

---

## 🔁 What's Next?
Continue to [LAB05 - Secrets & Volumes](../LAB05-Secrets-And-Volumes/) to secure your containers.

Push. Deploy. Relax. 🐳🚀🧩

