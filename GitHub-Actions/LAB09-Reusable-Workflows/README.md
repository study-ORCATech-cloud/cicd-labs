# LAB09 - Reusable Workflows (GitHub Actions)

This lab walks you through how to **create reusable workflows** using the `workflow_call` trigger in GitHub Actions — a powerful way to DRY (Don't Repeat Yourself) your CI/CD processes across multiple repositories or teams.

---

## 🎯 Objectives

By the end of this lab, you will:
- Define a reusable workflow template using `workflow_call`
- Call the workflow from another workflow file
- Centralize logic for builds, tests, or deployments

---

## 🧰 Prerequisites

- Two GitHub repositories:
  - `ci-templates` (for the reusable workflow)
  - `demo-project` (to consume the workflow)

---

## 🗂️ Folder Structure

```bash
GitHub-Actions/LAB09-Reusable-Workflows/
├── ci-templates/.github/workflows/template.yml
├── demo-project/.github/workflows/caller.yml
└── README.md
```

---

## 🚀 Getting Started

### In `ci-templates` repository

1. **Create the reusable workflow file:**
```yaml
# .github/workflows/template.yml
name: Reusable Template

on:
  workflow_call:

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello from reusable workflow!"
```

2. **Push this to `main` branch.**

---

### In `demo-project` repository

3. **Create the caller workflow:**
```yaml
# .github/workflows/caller.yml
name: Use Reusable Workflow

on:
  push:
    branches: [ main ]

jobs:
  call-template:
    uses: your-username/ci-templates/.github/workflows/template.yml@main
```

4. **Push and check the Actions tab.**

---

## ✅ Validation Checklist

- [ ] `template.yml` defined and accessible
- [ ] `caller.yml` correctly references the remote repo and branch
- [ ] Workflow runs and prints greeting from reusable job

---

## 🧹 Cleanup
- Delete workflows or repos when finished testing

---

## 🧠 Key Concepts

- Reusable workflows simplify team-wide standardization
- Only `workflow_call:` makes a workflow callable
- Parameters, outputs, and secrets can be shared

---

## 🔁 What’s Next?
Finish the GitHub Actions track with [LAB10 - Canary Deployment](../LAB10-Canary-Deployment/) to implement safer deployment strategies.

Write once. Reuse everywhere. 🧩📦🔁