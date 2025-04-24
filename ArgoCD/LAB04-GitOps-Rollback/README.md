# LAB04 - GitOps Rollback

## 📝 Description
In this lab, you’ll learn how to roll back application changes using **ArgoCD**, embracing the power of **GitOps** for safe, auditable, and reproducible rollbacks.

---

## 🎯 Objectives
- Understand ArgoCD revision history
- Roll back a deployed application to a previous state
- Use Git commits to trigger rollback operations

---

## 🧰 Prerequisites
- Completion of LAB03
- Working ArgoCD app with synced history
- GitHub repo access to update manifests

---

## 🗂️ Folder Structure
```bash
ArgoCD/LAB04-GitOps-Rollback/
├── manifests/
│   ├── deployment-v1.yaml
│   └── deployment-v2.yaml
├── argo-app.yaml
└── README.md
```

---

## 🚀 Getting Started

### 1. Deploy v1 of the app
Push `deployment-v1.yaml` to the repo and sync the app.

### 2. Upgrade to v2
Replace with `deployment-v2.yaml` and commit/push.
```bash
git add .
git commit -m "Upgrade to v2"
git push
```
Sync the ArgoCD app.

### 3. Rollback via UI or CLI
Use ArgoCD CLI or UI to roll back to v1.
```bash
argocd app history myapp
argocd app rollback myapp <REVISION-NUMBER>
```

---

## ✅ Validation Checklist
- [ ] Application deployed and upgraded
- [ ] Rollback triggered from ArgoCD UI or CLI
- [ ] App reverted to previous version

---

## 🧹 Cleanup
```bash
argocd app delete myapp --cascade
```

---

## 🧠 Key Concepts
- Git-based rollback using commit history
- Safe and traceable state management
- ArgoCD revision tracking

---

## 🔁 What's Next?
Continue to [LAB05 - Sync Policy Auto Sync](../LAB05-Sync-Policy-Auto-Sync/) to automate ArgoCD deployments.

Version control meets deployment control. 🔁🧬📂