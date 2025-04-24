# LAB06 - Service Health Checks (Docker-CD)

In this lab, you'll configure **health checks** in your Docker Compose setup to monitor the status of running containers and restart them automatically if they fail.

---

## 🎯 Objectives

By the end of this lab, you will:
- Define `healthcheck` instructions in Compose
- Monitor container status using `docker ps`
- Ensure services self-heal when they become unhealthy

---

## 🧰 Prerequisites

- Docker and Docker Compose
- A simple web app containerized with Flask

---

## 🗂️ Folder Structure

```bash
Docker-CD/LAB06-Service-Health-Checks/
├── app/
│   └── main.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### 1. Application:
```python
# app/main.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Health check passed"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 2. Dockerfile:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY app/ .
RUN pip install flask curl
CMD ["python", "main.py"]
```

### 3. Compose with health check:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:5000"]
      interval: 10s
      timeout: 5s
      retries: 3
```

### 4. Start the service:
```bash
docker-compose up --build
```

Use `docker ps` or `docker inspect <container_id>` to check health status.

---

## ✅ Validation Checklist

- [ ] Healthcheck defined and visible in Compose config
- [ ] Container shows `healthy` in status
- [ ] Logs or inspect confirm healthcheck execution

---

## 🧹 Cleanup
```bash
docker-compose down
```

---

## 🧠 Key Concepts

- Health checks monitor service uptime and stability
- Compose can define retries, intervals, and timeouts
- Docker's self-healing improves fault tolerance

---

## 🔁 What's Next?
Continue to [LAB07 - Microservices CI Pipeline](../LAB07-Microservices-CI-Pipeline/) to build pipelines for multi-container stacks.

Keep your services running strong. 💪🐳📈