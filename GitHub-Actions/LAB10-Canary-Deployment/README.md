# LAB10 - Canary Deployment (GitHub Actions)

In this advanced GitHub Actions lab, you'll implement a **canary deployment strategy**, where only a small subset of users receive a new version of the application initially, before rolling it out to everyone.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand the concept of canary deployments
- Use GitHub Actions to trigger separate `canary` and `production` workflows
- Use tags or environment branches to promote versions gradually

---

## 🧰 Prerequisites

- A GitHub repository
- Docker knowledge or Kubernetes knowledge (for real implementation)
- Two deployment environments: `canary` and `production`

---

## 🗂️ Folder Structure

```bash
GitHub-Actions/LAB10-Canary-Deployment/
├── .github/
│   └── workflows/
│       └── canary-deploy.yml
└── README.md
```

---

## 🚀 Getting Started

1. **Create the workflow:**
```yaml
# .github/workflows/canary-deploy.yml
name: Canary Deployment

on:
  push:
    tags:
      - 'v*.*.*-canary'

jobs:
  deploy-canary:
    runs-on: ubuntu-latest
    environment: canary
    steps:
      - uses: actions/checkout@v3
      - run: echo "🚀 Deploying canary version ${{ github.ref_name }} to canary environment"
```

2. **Create and push a canary tag:**
```bash
git tag v1.0.0-canary
git push origin v1.0.0-canary
```

3. **Observe the Actions tab and deploy log.**

4. **You could repeat the above with a different `production-deploy.yml` workflow for final release.**

---

## ✅ Validation Checklist

- [ ] Tag push triggers the canary deploy workflow
- [ ] Deployment is restricted to `canary` environment
- [ ] Logs confirm proper deployment execution

---

## 🧹 Cleanup
- Delete workflow or tags if no longer needed
- Use environments to restrict access for safety

---

## 🧠 Key Concepts

- Canary deployments allow testing in a partial environment
- Tags are useful for release workflows
- `environments:` in Actions provide approval gates, protections

---

## ✅ GitHub Actions Track Complete!
You’ve completed 10 hands-on labs covering everything from basic CI to real-world CD practices using GitHub Actions.

Explore Jenkins, Docker, or ArgoCD labs next to extend your DevOps pipeline mastery!

Deploy smart. Ship safe. Scale confidently. 🐥🚀📈