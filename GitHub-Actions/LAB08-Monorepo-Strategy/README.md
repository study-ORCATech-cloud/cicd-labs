# LAB08 - Monorepo Strategy (GitHub Actions)

This lab teaches you how to create **conditional workflows** in GitHub Actions that run based on which folder in a monorepo was modified. This is useful for large repositories with multiple apps or services.

---

## 🎯 Objectives

By the end of this lab, you will:
- Set up conditional workflows triggered only on path changes
- Use `if:` conditions and path filters
- Optimize workflows in monorepos

---

## 🧰 Prerequisites

- GitHub repo with at least two folders (e.g., `frontend/`, `backend/`)

---

## 🗂️ Folder Structure

```bash
GitHub-Actions/LAB08-Monorepo-Strategy/
├── .github/
│   └── workflows/
│       └── monorepo-check.yml
├── frontend/
│   └── index.html
├── backend/
│   └── app.py
└── README.md
```

---

## 🚀 Getting Started

1. **Create folders and basic files:**
```bash
mkdir frontend backend

echo "<h1>Hello Frontend</h1>" > frontend/index.html
echo "print('Hello Backend')" > backend/app.py
```

2. **Create a workflow to run jobs based on changed paths:**
```yaml
# .github/workflows/monorepo-check.yml
name: Monorepo Strategy

on:
  push:
    paths:
      - 'frontend/**'
      - 'backend/**'

jobs:
  frontend-job:
    if: contains(github.event.head_commit.message, 'frontend')
    runs-on: ubuntu-latest
    steps:
      - name: Run Frontend Job
        run: echo "Frontend task triggered."

  backend-job:
    if: contains(github.event.head_commit.message, 'backend')
    runs-on: ubuntu-latest
    steps:
      - name: Run Backend Job
        run: echo "Backend task triggered."
```

3. **Push commits and observe jobs run selectively.**

---

## ✅ Validation Checklist

- [ ] Commit message includes `frontend` or `backend`
- [ ] Only the relevant job runs in GitHub Actions
- [ ] Workflow triggers only on specific file changes

---

## 🧹 Cleanup
- Delete workflow or adjust paths as needed for real use cases

---

## 🧠 Key Concepts

- Path filters optimize monorepo CI usage
- `if:` conditions allow fine-grained control over jobs
- Useful for microservices, multi-package repos

---

## 🔁 What’s Next?
Continue to [LAB09 - Reusable Workflows](../LAB09-Reusable-Workflows/) to create shareable pipeline templates.

One repo. Many workflows. Built smart. 📦📁