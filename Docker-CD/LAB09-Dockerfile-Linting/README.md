# LAB09 - Dockerfile Linting (Docker-CD)

In this lab, you'll learn how to **lint and validate your Dockerfiles** using tools that check for best practices, security issues, and build optimizations.

---

## 🎯 Objectives

By the end of this lab, you will:
- Use a Dockerfile linter to catch common issues
- Automate linting via CI
- Improve Dockerfile quality and performance

---

## 🧰 Prerequisites

- Docker installed
- A Dockerfile-based project
- Optionally: Node.js and `npm` for installing CLI linters

---

## 🗂️ Folder Structure

```bash
Docker-CD/LAB09-Dockerfile-Linting/
├── app/
│   └── main.py
├── Dockerfile
├── README.md
└── .hadolint.yaml (optional config)
```

---

## 🚀 Getting Started

### 1. Install a linter (Hadolint or Dockerfilelint):
#### Hadolint via Docker:
```bash
docker run --rm -i hadolint/hadolint < Dockerfile
```

#### Or install locally:
```bash
brew install hadolint  # macOS
sudo apt install hadolint  # Debian/Ubuntu
```

### 2. Lint your Dockerfile:
```bash
hadolint Dockerfile
```

### 3. GitHub Actions workflow (optional):
```yaml
name: Dockerfile Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint Dockerfile
        run: docker run --rm -i hadolint/hadolint < Dockerfile
```

---

## ✅ Validation Checklist

- [ ] Linter installed and working
- [ ] Warnings/errors shown for poor patterns
- [ ] CI integration highlights issues in PRs

---

## 🧹 Cleanup
- No cleanup needed; linter runs on demand

---

## 🧠 Key Concepts

- Linters enforce Dockerfile quality and consistency
- Catch potential security risks early
- CI integration adds visibility and automation

---

## 🔁 What's Next?
Continue to [LAB10 - Logs Aggregation in CD](../LAB10-Logs-Aggregation-CD/) to centralize logs from multi-service apps.

Lint early. Build better. 🧼🐳🧪

