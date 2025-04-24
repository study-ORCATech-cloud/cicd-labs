# LAB07 - Staging To Production

## 📝 Description
This lab explores promoting changes from **staging** to **production** environments using Git branches or folders. You'll implement a multi-environment GitOps workflow with ArgoCD.

---

## 🎯 Objectives
- Set up separate environments (staging, production)
- Use Git structure (folders or branches) for multi-env
- Promote changes from staging to production

---

## 🧰 Prerequisites
- Completion of LAB06
- ArgoCD installed with access to Git repo
- Familiarity with branching strategies or folder structure

---

## 🗂️ Folder Structure
```bash
ArgoCD/LAB07-Staging-To-Production/
├── staging/
│   └── deployment.yaml
├── production/
│   └── deployment.yaml
├── argo-app-staging.yaml
├── argo-app-production.yaml
└── README.md
```

---

## 🚀 Getting Started

### 1. Set up folder structure in Git repo
Create `staging/` and `production/` folders, each with its own `deployment.yaml`.

### 2. Create ArgoCD apps for both environments
Apply the following two manifests:
```bash
kubectl apply -f argo-app-staging.yaml
kubectl apply -f argo-app-production.yaml
```

### 3. Promote changes
Edit the staging manifest, commit and push. Once verified, copy the change to production and push.

---

## ✅ Validation Checklist
- [ ] Git repo contains both `staging/` and `production/`
- [ ] Two ArgoCD apps appear in the UI
- [ ] Changes flow from staging to production by Git promotion

---

## 🧹 Cleanup
```bash
argocd app delete app-staging --cascade
argocd app delete app-production --cascade
```

---

## 🧠 Key Concepts
- Multi-environment deployments
- Git-based promotion strategies
- Environment separation using folders or branches

---

## 🔁 What's Next?
Continue to [LAB08 - CI Promote To ArgoCD](../LAB08-CI-Promote-To-ArgoCD/) to integrate CI pipelines with GitOps promotion workflows.

Staging approved? Promote to prod with Git. 🚦📂📦