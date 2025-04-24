# LAB05 - Secrets & Volumes (Docker-CD)

This lab shows how to securely inject **secrets** and configure **volumes** in Docker Compose. You'll learn to manage environment variables and sensitive values without hardcoding them.

---

## 🎯 Objectives

By the end of this lab, you will:
- Use `.env` files and Compose environment syntax
- Securely inject secrets using environment variables
- Mount volumes for data persistence

---

## 🧰 Prerequisites

- Docker and Docker Compose
- A basic Flask or Python app
- Basic understanding of `.env` files and Linux paths

---

## 🗂️ Folder Structure

```bash
Docker-CD/LAB05-Secrets-And-Volumes/
├── app/
│   └── main.py
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🚀 Getting Started

### 1. Create the app with an environment dependency:
```python
# app/main.py
import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    secret = os.getenv("APP_SECRET", "not-set")
    return f"Secret is: {secret}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 2. Dockerfile:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY app/ .
RUN pip install flask
CMD ["python", "main.py"]
```

### 3. Compose file with env + volume:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    volumes:
      - webdata:/data

volumes:
  webdata:
```

### 4. Add `.env` file:
```bash
APP_SECRET=super-secret-value
```

### 5. Start the service:
```bash
docker-compose up --build
```

Visit [http://localhost:5000](http://localhost:5000) and verify the secret.

---

## ✅ Validation Checklist

- [ ] Secret read from `.env` file
- [ ] Mounted volume `webdata` visible in `docker volume ls`
- [ ] App returns correct environment variable in browser

---

## 🧹 Cleanup
```bash
docker-compose down -v
```
Remove `.env` if storing sensitive data.

---

## 🧠 Key Concepts

- `.env` simplifies managing secrets per environment
- Volumes provide persistent storage for containers
- Avoid hardcoding secrets in Dockerfiles or code

---

## 🔁 What's Next?
Continue to [LAB06 - Service Health Checks](../LAB06-Service-Health-Checks/) to make sure your containers stay healthy.

Secure. Store. Scale. 🔐📦🧪

