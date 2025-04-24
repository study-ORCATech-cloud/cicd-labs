# LAB01 - Dockerfile Build (Docker-CD)

In this lab, you'll build a Docker image from a basic application using a `Dockerfile`. This foundational step enables containerized CI/CD workflows.

---

## 🎯 Objectives

By the end of this lab, you will:
- Write a simple `Dockerfile`
- Build a Docker image locally
- Tag and inspect the image

---

## 🧰 Prerequisites

- Docker installed and running locally
- A simple app in Python, Node.js, or any language

---

## 🗂️ Folder Structure

```bash
Docker-CD/LAB01-Dockerfile-Build/
├── app/
│   └── main.py
├── Dockerfile
└── README.md
```

---

## 🚀 Getting Started

1. **Create a simple app:**
```python
# app/main.py
print("Hello from Docker!")
```

2. **Write the Dockerfile:**
```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app/ .
CMD ["python", "main.py"]
```

3. **Build and tag the Docker image:**
```bash
docker build -t docker-lab-hello .
```

4. **Run the container:**
```bash
docker run --rm docker-lab-hello
```

---

## ✅ Validation Checklist

- [ ] Docker image builds successfully with `docker build`
- [ ] Container runs and prints the expected message
- [ ] Image appears in `docker images` list

---

## 🧹 Cleanup
```bash
docker image rm docker-lab-hello
```

---

## 🧠 Key Concepts

- A `Dockerfile` defines how to package an application
- Use `WORKDIR`, `COPY`, and `CMD` to set behavior
- `docker build` and `docker run` are the primary commands

---

## 🔁 What's Next?
Continue to [LAB02 - Compose CI Integration](../LAB02-Compose-CI-Integration/) to manage multi-container workflows.

Containerized and ready to scale. 🐳⚙️📦

