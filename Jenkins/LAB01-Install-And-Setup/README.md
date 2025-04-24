# LAB01 - Jenkins Install and Setup

In this first Jenkins lab, you’ll learn how to install Jenkins on your local machine (or in Docker) and access the Jenkins UI to start creating CI/CD jobs.

---

## 🎯 Objectives

By the end of this lab, you will:
- Install Jenkins via Docker or on your host system
- Access the Jenkins UI and unlock the admin panel
- Install essential plugins and configure initial settings

---

## 🧰 Prerequisites

- Docker installed (recommended)
- Or Java (JDK 11+) installed for native setup

---

## 🚀 Getting Started with Docker (Recommended)

1. **Create a Docker volume for Jenkins data:**
```bash
docker volume create jenkins-data
```

2. **Run Jenkins using Docker:**
```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins-data:/var/jenkins_home \
  jenkins/jenkins:lts
```

3. **Access Jenkins:**
Visit [http://localhost:8080](http://localhost:8080)

4. **Unlock Jenkins:**
Check the logs to find the admin password:
```bash
docker logs jenkins | grep 'Please use the following password'
```

5. **Install suggested plugins and create admin user.**

---

## 🖥️ Alternative: Native Installation
- Download Jenkins WAR or installer from [https://www.jenkins.io/download](https://www.jenkins.io/download)
- Run with:
```bash
java -jar jenkins.war
```
- Access on [http://localhost:8080](http://localhost:8080)

---

## ✅ Validation Checklist

- [ ] Jenkins is running on `localhost:8080`
- [ ] Admin password retrieved and entered
- [ ] Plugins installed and admin user created

---

## 🧹 Cleanup
```bash
docker stop jenkins && docker rm jenkins
```
Or remove the volume as well:
```bash
docker volume rm jenkins-data
```

---

## 🧠 Key Concepts

- Jenkins is an open-source automation server for CI/CD
- It runs on port 8080 and uses port 50000 for agents
- Docker is the easiest way to get started quickly

---

## 🔁 What's Next?
Continue to [LAB02 - Freestyle Python Job](../LAB02-Freestyle-Python-Job/) to create your first CI job manually.

Let’s get Jenkins up and running! 🛠️⚙️📦

