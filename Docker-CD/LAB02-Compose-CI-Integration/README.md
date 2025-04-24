# LAB02 - Docker Compose CI Integration (Docker-CD)

In this lab, you'll use **Docker Compose** to define and run a multi-container application. You'll then integrate this workflow into a CI system like GitHub Actions for automated testing and validation.

---

## 🎯 Objectives

By the end of this lab, you will:
- Define a multi-container app using `docker-compose.yml`
- Run Compose locally for dev or CI validation
- Optionally integrate the workflow into GitHub Actions

---

## 🧰 Prerequisites

- Docker and Docker Compose installed
- Basic knowledge of Docker networking

---

## 🗂️ Folder Structure

```bash
Docker-CD/LAB02-Compose-CI-Integration/
├── app/
│   └── main.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### 1. Create your service:
```python
# app/main.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Service running"

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

### 3. Compose file:
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
```

### 4. Run it locally:
```bash
docker-compose up --build
```

Visit [http://localhost:5000](http://localhost:5000) to test.

---

## ✅ Validation Checklist

- [ ] Compose file launches the app
- [ ] Service accessible on port 5000
- [ ] Flask server runs without error

---

## 🧹 Cleanup
```bash
docker-compose down
```

---

## 🧠 Key Concepts

- Docker Compose helps manage multi-container apps
- Compose can be integrated into CI tools easily
- Services defined declaratively with `docker-compose.yml`

---

## 🔁 What's Next?
Continue to [LAB03 - Compose for Dev Environments](../LAB03-Compose-Dev-Environments/) to add volumes and debugging tools.

Compose once, run anywhere. 🐳🔧🔁