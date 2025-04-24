# LAB02 - Python Test Workflow (GitHub Actions)

In this lab, you'll set up a GitHub Actions workflow that automatically runs tests for a Python project using `pytest`. You'll also learn to use a matrix strategy to test across multiple Python versions.

---

## 🎯 Objectives

By the end of this lab, you will:
- Use a GitHub Actions matrix to test against Python 3.8, 3.9, and 3.10
- Automatically install dependencies and run `pytest`
- View logs and results in the GitHub Actions UI

---

## 🧰 Prerequisites

- Python 3.8+ installed locally
- A GitHub repository with a Python app and tests
- `requirements.txt` and `tests/` folder available

---

## 🗂️ Folder Structure

```bash
GitHub-Actions/LAB02-Python-Test-Workflow/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── requirements.txt
├── app.py
├── tests/
│   └── test_app.py
└── README.md
```

---

## 🚀 Getting Started

1. **Create a Python file and a simple test:**
```python
# app.py

def add(a, b):
    return a + b
```
```python
# tests/test_app.py
from app import add

def test_add():
    assert add(2, 3) == 5
```

2. **Create `requirements.txt`:**
```bash
echo "pytest" > requirements.txt
```

3. **Create workflow file at `.github/workflows/python-tests.yml`:**
```yaml
name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

4. **Push your changes and observe the matrix run.**

---

## ✅ Validation Checklist

- [ ] Tests run for Python 3.8, 3.9, and 3.10
- [ ] `pytest` is installed and executed
- [ ] Output visible in GitHub Actions tab

---

## 🧹 Cleanup
Remove `.github/workflows/python-tests.yml` if needed:
```bash
rm .github/workflows/python-tests.yml
```

---

## 🧠 Key Concepts

- Matrix builds allow you to test against multiple environments
- `pytest` integrates easily with GitHub Actions
- `requirements.txt` keeps test dependencies manageable

---

## 🔁 What's Next?
Continue to [LAB03 - Docker Build and Push](../LAB03-Docker-Build-And-Push/) to learn how to build and publish Docker images using GitHub Actions.

Test early. Test often. CI for the win! 🧪🐍