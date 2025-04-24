# LAB09 - Slack Notifications in Jenkins

In this lab, you’ll configure Jenkins to send notifications to a **Slack channel** about the status of your CI/CD pipelines — especially useful for teams.

---

## 🎯 Objectives

By the end of this lab, you will:
- Set up the Slack plugin in Jenkins
- Create an incoming Slack webhook
- Configure Jenkinsfile to send pipeline status messages

---

## 🧰 Prerequisites

- Jenkins running
- A Slack workspace and access to create webhooks
- Slack Notifications Plugin installed in Jenkins

---

## 🚀 Slack Setup

1. Go to your Slack workspace → **Apps → Search for "Incoming Webhooks"**
2. Add the app → Create a new webhook → Select a channel → Copy webhook URL

---

## 🔧 Jenkins Configuration

1. Go to: **Manage Jenkins → Configure System**
2. Under **Slack**, configure:
   - **Workspace**: `https://yourworkspace.slack.com`
   - **Credential**: Create Secret Text using webhook URL
   - **Default channel**: `#ci-cd-notifications` (or your channel)

---

## 📄 Jenkinsfile Example
```groovy
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Building app...'
      }
    }
  }
  post {
    success {
      slackSend(channel: '#ci-cd-notifications', message: '✅ Build succeeded')
    }
    failure {
      slackSend(channel: '#ci-cd-notifications', message: '❌ Build failed')
    }
  }
}
```

---

## ✅ Validation Checklist

- [ ] Webhook successfully sends test message
- [ ] Jenkinsfile includes `slackSend` with `post` block
- [ ] Message appears in selected Slack channel

---

## 🧹 Cleanup
- Remove webhook from Slack app settings
- Remove Slack integration from Jenkins if unused

---

## 🧠 Key Concepts

- `slackSend` sends custom messages from Jenkins
- `post` section allows status-based notifications
- Keep teams updated in real time

---

## 🔁 What’s Next?
Continue to [LAB10 - SSH Deploy to Remote Server](../LAB10-SSH-Remote-Deploy/) to automate delivery to a production-like machine.

Ping your team. Stay in sync. 📣💬📦

