# LAB07 - Artifact Caching & Dependencies (GitHub Actions)

In this lab, you'll learn how to use **GitHub Actions caching and artifacts** to speed up CI workflows and persist build outputs across steps or jobs.

---

## 🎯 Objectives

By the end of this lab, you will:
- Cache dependencies to speed up installs (e.g., Python packages)
- Upload and download artifacts across steps or jobs
- Understand cache keys and restore strategies

---

## 🧰 Prerequisites

- A Python project with `requirements.txt`
- GitHub repo with Actions enabled

---

## 🗂️ Folder Structure

```bash
GitHub-Actions/LAB07-Artifact-Caching/
├── .github/
│   └── workflows/
│       └── cache-python.yml
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

1. **Create a `requirements.txt`:**
```bash
flask
requests
```

2. **Create the workflow file:**
```yaml
# .github/workflows/cache-python.yml
name: Cache Python Dependencies

on: [push]

jobs:
  cache-pip:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Cache pip dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Verify installed packages
        run: pip list
```

---

## ✅ Validation Checklist

- [ ] Cache hit on second run (check Action logs)
- [ ] Dependencies are installed from cache or fresh
- [ ] Package list shows expected tools (e.g., Flask)

---

## 🧹 Cleanup
- Delete `cache-python.yml` if no longer needed
- Clear cache in GitHub → Actions → Cache tab (optional)

---

## 🧠 Key Concepts

- Caching speeds up builds by avoiding repeated installs
- Cache keys depend on hashes of files like `requirements.txt`
- Artifacts (not shown here) allow transferring files between jobs

---

## 🔁 What’s Next?
Continue to [LAB08 - Monorepo Strategy](../LAB08-Monorepo-Strategy/) to manage large projects in a single repository.

Cache smart. Build fast. 🚀📦