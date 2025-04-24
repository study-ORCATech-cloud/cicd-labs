# LAB03 - Helm Deployments

## 📝 Description
In this lab, you’ll use **ArgoCD** to deploy an application defined using **Helm charts**. Helm helps manage complex Kubernetes manifests, and ArgoCD integrates natively with it.

---

## 🎯 Objectives
- Understand Helm basics in Kubernetes
- Deploy a Helm chart via ArgoCD
- Sync and monitor Helm-based applications

---

## 🧰 Prerequisites
- Completion of LAB02
- Helm CLI installed
- Running Kubernetes cluster with ArgoCD

---

## 🗂️ Folder Structure
```bash
ArgoCD/LAB03-Helm-Deployments/
├── chart/ (or public repo URL)
├── argo-app.yaml
└── README.md
```

---

## 🚀 Getting Started

### 1. Create or use a Helm chart
You can use an existing public Helm chart, such as nginx from Bitnami:
```
https://charts.bitnami.com/bitnami
```

Or create your own chart locally:
```bash
helm create myapp
```
Push the chart to your Git repo.

### 2. Create the ArgoCD application
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: helm-demo
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/YOUR_USERNAME/helm-demo.git
    targetRevision: HEAD
    path: myapp
    helm:
      valueFiles:
        - values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

```bash
kubectl apply -f argo-app.yaml
```

### 3. Sync and monitor
```bash
argocd app sync helm-demo
argocd app get helm-demo
```

---

## ✅ Validation Checklist
- [ ] Helm chart repo or folder exists
- [ ] ArgoCD application uses Helm source
- [ ] App syncs and deploys correctly

---

## 🧹 Cleanup
```bash
argocd app delete helm-demo --cascade
```

---

## 🧠 Key Concepts
- Helm charts as a packaging solution
- ArgoCD native Helm integration
- Custom values management with `valueFiles`

---

## 🔁 What's Next?
Continue to [LAB04 - GitOps Rollback](../LAB04-GitOps-Rollback/) to learn about rolling back changes in ArgoCD.

From manifests to charts—elevate your GitOps game. 📦🚀