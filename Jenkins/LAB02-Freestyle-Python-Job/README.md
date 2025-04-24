# LAB02 - Freestyle Python Job (Jenkins)

In this lab, you’ll create a **Freestyle project** in Jenkins that clones a Python repo, installs dependencies, and runs tests manually via the Jenkins UI.

---

## 🎯 Objectives

By the end of this lab, you will:
- Create a Freestyle job in Jenkins
- Pull code from a Git repository
- Run Python tests using a build step

---

## 🧰 Prerequisites

- Jenkins installed and running (see LAB01)
- Python installed on Jenkins host or in Docker container
- A GitHub repository with a basic Python project:
  - `app.py`
  - `requirements.txt`
  - `tests/test_app.py`

---

## 🚀 Getting Started

1. **Create a new Freestyle job in Jenkins:**
   - Name: `python-ci-job`
   - Type: Freestyle project

2. **Configure Source Code Management:**
   - Select **Git**
   - Enter your GitHub repository URL

3. **Add Build Steps:**
   - Execute shell command:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest
```

4. **Save and Build Now**
   - Monitor the console output to verify success

---

## ✅ Validation Checklist

- [ ] Jenkins job pulls code from GitHub
- [ ] Dependencies are installed successfully
- [ ] `pytest` runs and shows test results

---

## 🧹 Cleanup
- Delete job in Jenkins if not needed

---

## 🧠 Key Concepts

- Freestyle jobs are simple, manual CI tasks
- Jenkins executes shell commands as build steps
- Good for simple pipelines and experimentation

---

## 🔁 What’s Next?
Continue to [LAB03 - Declarative Pipeline with Jenkinsfile](../LAB03-Declarative-Pipeline/) to automate the same logic with a reusable Jenkinsfile.

CI doesn't have to be fancy — just effective! ⚙️🐍📄

