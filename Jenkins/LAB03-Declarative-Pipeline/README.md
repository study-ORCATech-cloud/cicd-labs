# LAB03 - Declarative Pipeline with Jenkinsfile

In this lab, you’ll use a **Jenkinsfile** to define a pipeline using the declarative syntax. This makes your CI/CD logic version-controlled and reusable across Jenkins instances.

---

## 🎯 Objectives

By the end of this lab, you will:
- Create a Jenkins pipeline job
- Use a `Jenkinsfile` stored in Git
- Define stages for install, test, and build

---

## 🧰 Prerequisites

- Jenkins installed and running
- A GitHub repository with:
  - `app.py`
  - `requirements.txt`
  - `tests/test_app.py`
  - `Jenkinsfile`

---

## 🚀 Jenkinsfile Example

Place this file in the root of your repo:
```groovy
pipeline {
  agent any

  stages {
    stage('Install') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Test') {
      steps {
        sh 'pytest'
      }
    }
  }
}
```

---

## 🧪 Job Configuration in Jenkins

1. Go to Jenkins → New Item → Pipeline
2. Name: `python-pipeline`
3. Under **Pipeline → Definition**, select **Pipeline script from SCM**
4. SCM: **Git**
5. Repository URL: your GitHub repo with `Jenkinsfile`
6. Script Path: `Jenkinsfile`
7. Save and click **Build Now**

---

## ✅ Validation Checklist

- [ ] Job pulls code from GitHub
- [ ] Pipeline shows install and test stages
- [ ] Output from each step is visible

---

## 🧹 Cleanup
- Delete the job or Jenkinsfile if needed

---

## 🧠 Key Concepts

- Declarative pipelines use a simple `pipeline {}` syntax
- Jenkinsfile makes pipelines version-controlled
- Each `stage {}` represents a step in your process

---

## 🔁 What’s Next?
Continue to [LAB04 - SCM Polling & Webhooks](../LAB04-SCM-Polling-Webhooks/) to trigger builds automatically when code is pushed.

Script it once. Reuse forever. 🧪⚙️📁

