# LAB03 - Compose for Dev Environments (Docker-CD)

In this lab, you’ll configure **Docker Compose** for local development environments, using volumes and mounted source code for real-time edits and debugging.

---

## 🎯 Objectives

By the end of this lab, you will:
- Use volume mounts in Docker Compose for hot-reloading
- Develop your app locally in containers without rebuilding
- Set up a persistent containerized dev workflow

---

## 🧰 Prerequisites

- Docker and Docker Compose
- Basic Python/Flask app
- Familiarity with file paths and editors

---

## 🗂️ Folder Structure

```bash
Docker-CD/LAB03-Compose-Dev-Environments/
├── app/
│   └── main.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### 1. Application (same as previous lab):
```python
# app/main.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Development environment ready!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 2. Dockerfile:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY app/ .
RUN pip install flask
CMD ["python", "main.py"]
```

### 3. Compose file with volume mount:
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./app:/app
```

### 4. Run with Compose:
```bash
docker-compose up
```

Modify `app/main.py` locally and see changes immediately (no rebuild needed).

---

## ✅ Validation Checklist

- [ ] Volume mount maps your local code into the container
- [ ] App reloads on file change
- [ ] Dev workflow runs smoothly in Compose

---

## 🧹 Cleanup
```bash
docker-compose down
```

---

## 🧠 Key Concepts

- Volume mounts sync local code into containers
- Ideal for iterative development and debugging
- Compose helps isolate and manage dev environments

---

## 🔁 What's Next?
Continue to [LAB04 - Deploy with GitHub Actions](../LAB04-Deploy-With-GitHub-Actions/) to integrate Compose with CI/CD.

Develop live, containerized and clean. 🛠️🐳💻