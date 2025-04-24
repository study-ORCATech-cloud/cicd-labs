# LAB04 - Deploy to GitHub Pages (Static Site CD)

In this lab, you'll set up a GitHub Actions workflow to **build and deploy a static website** (like a portfolio or documentation site) to **GitHub Pages**.

---

## 🎯 Objectives

By the end of this lab, you will:
- Automatically deploy static content on every push
- Use the `actions/deploy-pages` action
- Configure your repo to publish from the `gh-pages` branch

---

## 🧰 Prerequisites

- GitHub repository (public or private)
- Simple HTML site or static generator (Jekyll, Docusaurus, etc.)
- GitHub Pages enabled for the repository (Settings → Pages)

---

## 🗂️ Folder Structure

```bash
GitHub-Actions/LAB04-Deploy-GitHub-Pages/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml
├── site/
│   └── index.html
└── README.md
```

---

## 🚀 Getting Started

1. **Create a simple HTML page:**
```html
<!-- site/index.html -->
<!DOCTYPE html>
<html>
<head><title>Hello Pages</title></head>
<body><h1>Deployed with GitHub Actions!</h1></body>
</html>
```

2. **Create a workflow file at `.github/workflows/deploy-pages.yml`:**
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Pages
        uses: actions/configure-pages@v3

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: './site'

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v2
```

3. **Go to your GitHub repo → Settings → Pages → Select "GitHub Actions" as source.**

4. **Push to `main` and visit your GitHub Pages site!**

---

## ✅ Validation Checklist

- [ ] GitHub Pages enabled
- [ ] Site deployed automatically on push
- [ ] Workflow succeeded in Actions tab
- [ ] Page is publicly accessible via GitHub Pages URL

---

## 🧹 Cleanup
- Disable GitHub Pages or delete `.github/workflows/deploy-pages.yml`

---

## 🧠 Key Concepts

- `actions/deploy-pages` simplifies static site deployment
- GitHub Pages works with public and private repos
- Good for portfolios, docs, single-page sites

---

## 🔁 What's Next?
Continue to [LAB05 - Scheduled Jobs & Cron Triggers](../LAB05-Scheduled-Cron-Jobs/) to automate jobs that run on a schedule.

Serve your site with a single push. 🌐🚀📄