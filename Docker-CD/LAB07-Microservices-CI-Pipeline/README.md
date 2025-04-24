# LAB07 - Microservices CI Pipeline (Docker-CD)

In this lab, you'll build a **CI pipeline for a multi-service application** using Docker Compose. Each service will be tested independently and validated in a shared network context.

---

## 🎯 Objectives

By the end of this lab, you will:
- Build and test multiple services using Compose
- Validate service interactions within a CI pipeline
- Structure containerized microservices for automation

---

## 🧰 Prerequisites

- Docker and Docker Compose installed
- Basic Python/Node.js app templates for testing
- GitHub Actions or other CI tool (optional integration)

---

## 🗂️ Folder Structure

```bash
Docker-CD/LAB07-Microservices-CI-Pipeline/
├── service1/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── service2/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### Example service1:
```python
# service1/app.py
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index(): return "Hello from Service 1"
```

### Example service2:
```python
# service2/app.py
from flask import Flask
import requests
app = Flask(__name__)
@app.route('/')
def index():
    r = requests.get("http://service1:5000")
    return f"Service 2 says: {r.text}"
```

### docker-compose.yml:
```yaml
version: '3.8'
services:
  service1:
    build: ./service1
    ports:
      - "5001:5000"
  service2:
    build: ./service2
    ports:
      - "5002:5000"
    depends_on:
      - service1
```

### Run it locally:
```bash
docker-compose up --build
```

Visit `http://localhost:5002` to confirm service chaining.

---

## ✅ Validation Checklist

- [ ] Compose builds both services without error
- [ ] `service2` successfully calls `service1`
- [ ] Logs confirm request-response flow

---

## 🧹 Cleanup
```bash
docker-compose down
```

---

## 🧠 Key Concepts

- Compose enables isolated, networked services
- `depends_on` ensures startup order (not health)
- Service chaining is essential for integration testing

---

## 🔁 What's Next?
Continue to [LAB08 - Deploy to ECS](../LAB08-Deploy-To-ECS/) to take your Compose stack to the cloud.

Microservices, one pipeline at a time. ⚙️🔄🐳