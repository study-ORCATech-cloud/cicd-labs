# LAB06 - Secrets & Contexts (GitHub Actions)

In this lab, you’ll learn how to securely use **secrets** and **contexts** in GitHub Actions to protect sensitive data and dynamically access runtime metadata.

---

## 🎯 Objectives

By the end of this lab, you will:
- Store and use encrypted secrets in a workflow
- Use contexts like `github`, `env`, and `runner`
- Securely pass data into steps without hardcoding

---

## 🧰 Prerequisites

- GitHub repository with Actions enabled
- Create a secret under repo settings: `MY_SECRET_VALUE = super-secret`

---

## 🗂️ Folder Structure

```bash
GitHub-Actions/LAB06-Secrets-And-Contexts/
├── .github/
│   └── workflows/
│       └── show-secrets.yml
└── README.md
```

---

## 🚀 Getting Started

1. **Create a workflow file:**
```yaml
# .github/workflows/show-secrets.yml
name: Secrets & Contexts Demo

on:
  push:
    branches: [ main ]

jobs:
  context-demo:
    runs-on: ubuntu-latest
    env:
      USER_ENV: demo-user

    steps:
      - name: Print GitHub context
        run: echo "Triggered by ${{ github.actor }} on repo ${{ github.repository }}"

      - name: Print environment variable
        run: echo "Using environment: $USER_ENV"

      - name: Use secret value (secure)
        run: echo "Secret length: ${#MY_SECRET_VALUE}"
        env:
          MY_SECRET_VALUE: ${{ secrets.MY_SECRET_VALUE }}
```

2. **Push to `main` and check the Actions logs.**
> 🛑 Do not echo full secrets! Only show properties like length.

---

## ✅ Validation Checklist

- [ ] Secret stored and passed securely
- [ ] Context values like `github.actor` printed correctly
- [ ] `env:` variables available to steps

---

## 🧹 Cleanup
- Delete the secret from GitHub if no longer needed
- Remove workflow if just testing: `rm .github/workflows/show-secrets.yml`

---

## 🧠 Key Concepts

- Secrets are encrypted at rest and never printed by default
- Contexts let you access useful metadata inside workflows
- `env:` injects environment variables for any step or job

---

## 🔁 What’s Next?
Continue to [LAB07 - Artifact Caching](../LAB07-Artifact-Caching/) to speed up workflows with dependency caching.

Secure it. Access it. Context matters. 🔐📦⚙️