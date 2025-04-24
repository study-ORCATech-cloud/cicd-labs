# LAB05 - Sync Policy Auto Sync

## 📝 Description
In this lab, you’ll configure **ArgoCD** to automatically synchronize applications with Git using **auto-sync policies**. This ensures your cluster state always reflects the latest committed Git configuration.

---

## 🎯 Objectives
- Enable automated sync policy in ArgoCD
- Test auto-deployments on Git updates
- Understand sync strategies (prune, self-heal)

---

## 🧰 Prerequisites
- Completion of LAB04
- GitHub repo with working ArgoCD Application

---

## 🗂️ Folder Structure
```bash
ArgoCD/LAB05-Sync-Policy-Auto-Sync/
├── manifests/
│   └── deployment.yaml
├── argo-app.yaml
└── README.md
```

---

## 🚀 Getting Started

### 1. Update the ArgoCD app definition
Add the sync policy to `argo-app.yaml`:
```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
```

### 2. Apply the updated manifest
```bash
kubectl apply -f argo-app.yaml
```

### 3. Trigger auto-sync with Git changes
Modify the deployment (e.g., change replica count), commit and push to Git.
```yaml
replicas: 3
```
Check the ArgoCD UI or CLI:
```bash
argocd app get myapp
```

---

## ✅ Validation Checklist
- [ ] Auto-sync policy applied
- [ ] Git change triggered auto deployment
- [ ] ArgoCD status reflects auto-sync success

---

## 🧹 Cleanup
```bash
argocd app delete myapp --cascade
```

---

## 🧠 Key Concepts
- Auto-sync ensures Git is always source of truth
- `prune`: removes non-tracked resources
- `selfHeal`: reverts drifted resources

---

## 🔁 What's Next?
Continue to [LAB06 - Secrets Integration](../LAB06-Secrets-Integration/) to integrate secrets management with ArgoCD.

From clicks to commits—let Git deploy for you. 🔄📦🤖