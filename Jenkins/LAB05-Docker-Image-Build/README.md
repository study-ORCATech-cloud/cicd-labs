# LAB05 - Docker Image Build in Jenkins

In this lab, you’ll use Jenkins to build a Docker image from a `Dockerfile` and optionally push it to Docker Hub or a private registry.

---

## 🎯 Objectives

By the end of this lab, you will:
- Set up a Jenkins pipeline to build a Docker image
- Configure Docker inside Jenkins (locally or in a Docker agent)
- Tag and optionally push the image to a container registry

---

## 🧰 Prerequisites

- Jenkins host with Docker installed (or Jenkins running with Docker socket access)
- A GitHub repo with:
  - `Dockerfile`
  - Sample app (e.g., `app.py`)
- Optional: Docker Hub account and credentials added to Jenkins

---

## 🚀 Jenkinsfile Example

```groovy
pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          docker.build('my-python-app:latest')
        }
      }
    }

    stage('Run Container (optional)') {
      steps {
        sh 'docker run --rm my-python-app:latest'
      }
    }
  }
}
```

> Make sure Jenkins can access Docker commands. Mount `/var/run/docker.sock` if running Jenkins in Docker.

---

## ✅ Validation Checklist

- [ ] Docker image builds successfully via Jenkins pipeline
- [ ] Optional: container runs and shows output in logs
- [ ] Optional: image pushed to registry

---

## 🧹 Cleanup
- Remove unused images: `docker image prune -f`
- Stop/delete Jenkins job if not needed

---

## 🧠 Key Concepts

- Jenkins can build Docker images as part of pipelines
- Requires Docker access on agent machine
- `docker.build()` is Groovy shorthand for CLI commands

---

## 🔁 What’s Next?
Continue to [LAB06 - Parallel and Conditional Stages](../LAB06-Parallel-And-Conditional/) to structure more dynamic pipelines.

Containerize with confidence. 🐳⚙️🚀

