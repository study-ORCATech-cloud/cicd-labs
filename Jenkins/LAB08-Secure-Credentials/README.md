# LAB08 - Secure Credentials in Jenkins

In this lab, you’ll use Jenkins’ **Credentials plugin** to store and inject secrets such as API tokens, passwords, and SSH keys into your pipelines securely.

---

## 🎯 Objectives

By the end of this lab, you will:
- Store credentials using Jenkins Credentials Manager
- Inject credentials into a pipeline using `environment` or `withCredentials` block
- Mask credentials from job output

---

## 🧰 Prerequisites

- Jenkins installed and running
- Jenkins Credentials Plugin enabled (default)
- Jenkinsfile and test token/password for simulation

---

## 🚀 Adding a Credential

1. Jenkins → **Manage Jenkins → Credentials → (Global)**
2. Add Credentials:
   - **Type:** Secret Text
   - **ID:** `MY_API_TOKEN`
   - **Secret:** `super-secret-token`

---

## 📄 Example Jenkinsfile
```groovy
pipeline {
  agent any
  environment {
    API_TOKEN = credentials('MY_API_TOKEN')
  }
  stages {
    stage('Use Token') {
      steps {
        sh 'echo "Using secret token: $API_TOKEN"'
      }
    }
  }
}
```
> Token will be masked in output automatically. Never echo secrets in plaintext.

---

## ✅ Validation Checklist

- [ ] Credential added to Jenkins via UI
- [ ] Pipeline runs and accesses `API_TOKEN`
- [ ] Secret is **masked** in console output

---

## 🧹 Cleanup
- Delete the secret from **Manage Jenkins → Credentials** if no longer needed

---

## 🧠 Key Concepts

- `credentials('id')` loads secrets into environment vars
- Secure values are masked from logs
- Avoid hardcoding passwords in Jenkinsfiles

---

## 🔁 What’s Next?
Continue to [LAB09 - Slack Notifications](../LAB09-Slack-Notifications/) to notify your team of pipeline events.

Store it safe. Inject it smart. 🔐⚙️📣

