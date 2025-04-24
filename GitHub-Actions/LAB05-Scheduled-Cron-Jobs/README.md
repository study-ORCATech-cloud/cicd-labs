# LAB05 - Scheduled Jobs & Cron Triggers (GitHub Actions)

This lab shows how to schedule GitHub Actions workflows using `cron` syntax — ideal for tasks like nightly builds, weekly backups, or recurring checks.

---

## 🎯 Objectives

By the end of this lab, you will:
- Use `on: schedule:` in a GitHub Actions workflow
- Configure cron syntax for time-based automation
- Create a workflow that runs hourly or daily

---

## 🧰 Prerequisites

- GitHub account and repository access
- Basic YAML and cron syntax familiarity

---

## 🗂️ Folder Structure

```bash
GitHub-Actions/LAB05-Scheduled-Cron-Jobs/
├── .github/
│   └── workflows/
│       └── scheduled-task.yml
└── README.md
```

---

## 🚀 Getting Started

1. **Create a new workflow file at `.github/workflows/scheduled-task.yml`:**
```yaml
name: Scheduled Task

on:
  schedule:
    - cron: '0 * * * *'  # Every hour on the hour (UTC)

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Print timestamp
        run: echo "⏰ This job ran at $(date -u)"
```

2. **Push this workflow to GitHub.**

3. **Monitor the Actions tab after the cron interval passes.**

---

## ✅ Validation Checklist

- [ ] Workflow contains valid `cron` expression
- [ ] Action runs automatically according to schedule
- [ ] Logs show expected time of execution

---

## 🧹 Cleanup
- Delete `.github/workflows/scheduled-task.yml` to stop automation

---

## 🧠 Key Concepts

- GitHub uses UTC for cron expressions
- Use sites like [crontab.guru](https://crontab.guru/) for cron help
- Ideal for backups, reminders, and daily reports

---

## 🔁 What's Next?
Move on to [LAB06 - Secrets and Contexts](../LAB06-Secrets-And-Contexts/) to secure workflows and access runtime variables.

Automate on time — every time. 🕒📈🔁

