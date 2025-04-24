# LAB01 - Hello World Workflow (GitHub Actions)

In this first GitHub Actions lab, you'll create a simple workflow that runs on every code push. You'll learn how workflows are triggered, how jobs and steps are structured, and how to view logs from the Actions UI.

This foundational lab sets the stage for more complex CI/CD tasks.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand the basic structure of a GitHub Actions workflow
- Trigger a workflow on push to `main`
- Run a simple job that prints messages and environment variables

---

## 🧰 Prerequisites

- A GitHub account
- A Git repository with write access (new or existing)

---

## 🗂️ Folder Structure

```bash
GitHub-Actions/LAB01-Hello-World/
├── .github/
│   └── workflows/
│       └── hello-world.yml
└── README.md
```

---

## 🚀 Getting Started

1. **Create the required folders:**
```bash
mkdir -p .github/workflows
```

2. **Create a new file at `.github/workflows/hello-world.yml` with the following content:**
```yaml
name: Hello World CI

on:
  push:
    branches:
      - main

jobs:
  say-hello:
    runs-on: ubuntu-latest
    steps:
      - name: Echo greeting
        run: echo "👋 Hello from GitHub Actions!"

      - name: Show date and runner OS
        run: |
          echo "📅 Date: $(date)"
          echo "🖥️ Running on: ${{ runner.os }}"
```

3. **Commit and push your changes:**
```bash
git add .github/workflows/hello-world.yml
git commit -m "Add Hello World GitHub Actions workflow"
git push origin main
```

4. **Go to the 'Actions' tab in your GitHub repo to view the workflow run.**

---

## ✅ Validation Checklist

- [ ] Workflow file exists at `.github/workflows/hello-world.yml`
- [ ] Push to `main` triggers the workflow
- [ ] Steps run and show logs in the Actions tab
- [ ] Output includes greeting, date, and runner OS

---

## 🧹 Cleanup
To remove this workflow:
```bash
rm -rf .github/
```
Commit and push the deletion.

---

## 🧠 Key Concepts

- A **workflow** is triggered by GitHub events (e.g., push, pull_request)
- **Jobs** run on virtual machines (runners)
- **Steps** are individual commands executed in a job

---

## 🔁 What's Next?
Move on to [LAB02 - Python Test Workflow](../LAB02-Python-Test-Workflow/) to build a CI pipeline for testing Python code.

Hello world today, CI master tomorrow! 🌍🚀