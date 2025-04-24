# LAB10 - SSH Deploy to Remote Server (Jenkins)

In this final Jenkins lab, you’ll automate deployment to a remote server via **SSH**. This approach is commonly used for simple VM-based deployments or legacy environments.

---

## 🎯 Objectives

By the end of this lab, you will:
- Configure Jenkins to use SSH credentials
- Securely connect to a remote host and deploy an app
- Use `ssh-agent` and `scp` to transfer files and run commands remotely

---

## 🧰 Prerequisites

- A remote Linux server (e.g., AWS EC2, local VM)
- SSH key pair (public key added to remote `~/.ssh/authorized_keys`)
- Jenkins running and Credentials Plugin enabled

---

## 🔧 Jenkins Credentials Setup

1. Jenkins → **Manage Jenkins → Credentials → (Global)**
2. Add credentials:
   - **Kind**: SSH Username with private key
   - **ID**: `prod-ssh-key`
   - **Username**: `ec2-user` or similar
   - **Private Key**: Enter directly or upload

---

## 📄 Jenkinsfile Example
```groovy
pipeline {
  agent any

  stages {
    stage('Deploy via SSH') {
      steps {
        sshagent(['prod-ssh-key']) {
          sh 'scp app.py ec2-user@your-server-ip:/home/ec2-user/app.py'
          sh 'ssh ec2-user@your-server-ip "python3 /home/ec2-user/app.py"'
        }
      }
    }
  }
}
```

---

## ✅ Validation Checklist

- [ ] SSH credentials added in Jenkins
- [ ] Jenkins job uses `sshagent` block
- [ ] File copied and executed on remote machine

---

## 🧹 Cleanup
- Remove SSH credentials if temporary
- Clear remote app files manually if needed

---

## 🧠 Key Concepts

- `sshagent` lets Jenkins use SSH keys securely
- `scp` copies files; `ssh` runs remote commands
- Ideal for VM-based environments or simple servers

---

## 🎉 Jenkins Track Complete!
You’ve built, tested, containerized, and deployed with Jenkins using modern CI/CD practices. 🚀

Explore the **Docker-CD** or **ArgoCD** tracks next to expand your delivery pipeline expertise!

Deliver anywhere. From Jenkins with love. 📦💻🔑

