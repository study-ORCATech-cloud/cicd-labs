# LAB10 - Logs Aggregation in CD (Docker-CD)

In this lab, you’ll learn how to **aggregate and manage logs** from multiple Docker services during deployment, using Docker Compose with centralized log collection.

---

## 🎯 Objectives

By the end of this lab, you will:
- Use logging drivers in Compose
- Aggregate logs to a file or external tool
- Monitor logs for all services in a single stream

---

## 🧰 Prerequisites

- Docker and Docker Compose
- Basic logging knowledge
- Optional: Fluentd, Logstash, or Loki for external tools

---

## 🗂️ Folder Structure

```bash
Docker-CD/LAB10-Logs-Aggregation-CD/
├── service1/
│   └── app.py
├── service2/
│   └── app.py
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### 1. Example services with print logging:
```python
# service1/app.py
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    print("Service 1 received request")
    return "OK"

# service2/app.py (similar print statement)
```

### 2. Compose file with `json-file` logging:
```yaml
version: '3.8'
services:
  service1:
    build: ./service1
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
  service2:
    build: ./service2
    logging:
      driver: "json-file"
```

### 3. Start services:
```bash
docker-compose up --build
```

### 4. View logs:
```bash
docker-compose logs -f
```
Or for individual containers:
```bash
docker logs <container_id>
```

---

## ✅ Validation Checklist

- [ ] Logs written in a structured format (JSON)
- [ ] `docker-compose logs` aggregates all service logs
- [ ] Log retention and rotation configured

---

## 🧹 Cleanup
```bash
docker-compose down
```
Optionally clear logs:
```bash
docker system prune -af
```

---

## 🧠 Key Concepts

- Docker supports multiple logging drivers
- `json-file` is default and supports rotation
- Compose provides a unified view of logs for debugging

---

## 🎉 Docker-CD Track Complete!
You’ve built, tested, deployed, secured, and monitored containerized services with Docker and Docker Compose. Well done! 🐳🎓

Keep building with ArgoCD or Jenkins to level up your CD skills!

