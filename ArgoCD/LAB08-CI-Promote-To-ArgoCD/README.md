# LAB08 - CI Promote To ArgoCD

## 📝 Description
In this lab, you’ll simulate a **CI/CD pipeline** that updates Kubernetes manifests or Helm values in Git, and automatically triggers ArgoCD to deploy the updated application.

---

## 🎯 Objectives
- Understand how CI can promote artifacts to Git
- Trigger ArgoCD deployments via GitOps
- Automate a Git commit and sync workflow

---

## 🧰 Prerequisites
- Completion of LAB07
- GitHub repo connected to ArgoCD
- Basic GitHub Actions or CI knowledge

---

## 🗂️ Folder Structure
```bash
ArgoCD/LAB08-CI-Promote-To-ArgoCD/
├── manifests/
│   └── deployment.yaml
├── .github/workflows/
│   └── promote.yml
├── argo-app.yaml
└── README.md
```

---

## 🚀 Getting Started

### 1. Set up the GitHub Actions workflow
Create `.github/workflows/promote.yml`:
```yaml
name: Promote To ArgoCD
on:
  push:
    branches:
      - main
jobs:
  promote:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Update image tag
        run: |
          sed -i 's/tag: .*/tag: v2/' manifests/deployment.yaml
          git config user.name "ci-bot"
          git config user.email "ci@example.com"
          git commit -am "Promote to v2"
          git push
```

### 2. Push and observe ArgoCD
Push the changes and watch ArgoCD automatically sync and deploy the new version.

---

## ✅ Validation Checklist
- [ ] GitHub Actions workflow committed and runs on push
- [ ] ArgoCD app synced after CI push
- [ ] New version is deployed in the cluster

---

## 🧹 Cleanup
```bash
argocd app delete myapp --cascade
```

---

## 🧠 Key Concepts
- CI triggers GitOps via Git push
- GitOps enables auditability and rollback
- GitHub Actions as a CI mechanism

---

## 🔁 What's Next?
Continue to [LAB09 - Notifications](../LAB09-Notifications/) to learn how to alert on ArgoCD events.

CI meets GitOps—automate all the way. ⚙️📤🚀