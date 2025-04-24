# LAB06 - Parallel & Conditional Stages (Jenkins)

This lab focuses on creating Jenkins pipelines with **parallel execution** and **conditional logic**, making your CI/CD jobs faster and smarter.

---

## 🎯 Objectives

By the end of this lab, you will:
- Define parallel stages in a Jenkins pipeline
- Use conditional statements to skip or run stages based on parameters or environment

---

## 🧰 Prerequisites

- Jenkins with pipeline plugin installed
- A GitHub repo with a `Jenkinsfile`
- Basic shell commands or scripts for demo purposes

---

## 🚀 Jenkinsfile Example

```groovy
pipeline {
  agent any

  parameters {
    booleanParam(name: 'RUN_BACKEND', defaultValue: true, description: 'Run backend tests')
    booleanParam(name: 'RUN_FRONTEND', defaultValue: true, description: 'Run frontend tests')
  }

  stages {
    stage('Parallel Tests') {
      parallel {
        stage('Frontend Tests') {
          when {
            expression { return params.RUN_FRONTEND }
          }
          steps {
            echo 'Running frontend tests...'
          }
        }

        stage('Backend Tests') {
          when {
            expression { return params.RUN_BACKEND }
          }
          steps {
            echo 'Running backend tests...'
          }
        }
      }
    }
  }
}
```

---

## ✅ Validation Checklist

- [ ] Jenkins job accepts parameters for conditional execution
- [ ] Frontend and backend stages run in parallel
- [ ] Stages are skipped if unchecked

---

## 🧹 Cleanup
- Delete the job if it's for demo only
- Unset parameters if no longer needed

---

## 🧠 Key Concepts

- `parallel {}` runs multiple branches at the same time
- `when {}` adds flexibility to skip jobs dynamically
- Great for microservices or split test environments

---

## 🔁 What’s Next?
Continue to [LAB07 - Shared Libraries in Jenkins](../LAB07-Shared-Libraries/) to modularize pipeline logic for reusability.

Smarter, faster pipelines — done right. 🧠⚙️🧪

