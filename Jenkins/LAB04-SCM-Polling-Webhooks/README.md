# LAB04 - SCM Polling & Webhooks (Jenkins)

In this lab, you’ll trigger Jenkins pipeline jobs automatically based on changes in a GitHub repository — using either **polling** or **webhooks**.

---

## 🎯 Objectives

By the end of this lab, you will:
- Configure Jenkins to poll GitHub for changes
- Optionally configure a GitHub webhook to notify Jenkins instantly

---

## 🧰 Prerequisites

- Jenkins running and accessible
- A GitHub repo with a Jenkinsfile
- Jenkins URL exposed via tunnel or public IP (for webhooks)

---

## 🚀 Option A: SCM Polling

1. Open your Jenkins Pipeline job → **Configure**
2. Scroll to **Build Triggers** → Check **Poll SCM**
3. Schedule example (every 2 minutes):
```
H/2 * * * *
```
4. Save and push a commit to trigger a build within 2 minutes.

---

## 🚀 Option B: GitHub Webhook (Faster, Recommended)

1. In Jenkins → Job → Configure → Check **GitHub hook trigger for GITScm polling**
2. In GitHub → Repo → Settings → Webhooks → Add Webhook
   - **Payload URL:** `http://<your-public-jenkins-url>/github-webhook/`
   - **Content type:** `application/json`
   - Enable: Push events
3. Click Save. Push code to GitHub to trigger.

If you need a public URL, use [ngrok](https://ngrok.com/):
```bash
ngrok http 8080
```

---

## ✅ Validation Checklist

- [ ] Polling interval or webhook triggers the job
- [ ] Commit push results in Jenkins build
- [ ] Logs show updated pipeline run

---

## 🧹 Cleanup
- Uncheck triggers in Jenkins job config
- Delete GitHub webhook if no longer needed

---

## 🧠 Key Concepts

- SCM polling is time-based (cron-style)
- Webhooks are real-time and more efficient
- Jenkins must be reachable from GitHub for webhooks

---

## 🔁 What’s Next?
Continue to [LAB05 - Docker Image Build in Jenkins](../LAB05-Docker-Image-Build/) to build Docker images in your CI pipeline.

Trigger automatically. Build immediately. 🔄🐙🚀

