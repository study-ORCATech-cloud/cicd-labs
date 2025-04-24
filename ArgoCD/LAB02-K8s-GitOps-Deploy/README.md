# LAB02 - K8s GitOps Deploy

## 📝 Description
This lab demonstrates how to deploy a Kubernetes application using ArgoCD with GitOps principles. You'll create a Git repository with Kubernetes manifests and configure ArgoCD to continuously sync and deploy your app based on changes in Git.

---

## 🎯 Objectives
- Host application manifests in a Git repository
- Create an ArgoCD Application manifest
- Deploy an app via ArgoCD using GitOps methodology
- Understand ArgoCD's sync and app status

---

## 🧰 Prerequisites
- Completion of LAB01
- Public or private Git repository with access
- Kubernetes cluster and ArgoCD running
- `kubectl` and `argocd` CLI

---

## 🗂️ Folder Structure
```bash
ArgoCD/LAB02-K8s-GitOps-Deploy/
├── manifests/
│   ├── deployment.yaml
│   └── service.yaml
├── argo-app.yaml
└── README.md
```

---

## 🚀 Getting Started

### 1. Prepare the Git repository
Create a repo named `k8s-gitops-app` and include:

#### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo-app
  template:
    metadata:
      labels:
        app: demo-app
    spec:
      containers:
      - name: demo-app
        image: nginx:alpine
        ports:
        - containerPort: 80
```

#### service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-app-service
spec:
  type: LoadBalancer
  selector:
    app: demo-app
  ports:
    - port: 80
      targetPort: 80
```

### 2. Define the ArgoCD application
#### argo-app.yaml
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: demo-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/YOUR_USERNAME/k8s-gitops-app.git
    targetRevision: HEAD
    path: manifests
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

### 3. Sync the application
```bash
argocd app sync demo-app
```

### 4. Verify deployment
```bash
kubectl get pods -l app=demo-app
kubectl get svc demo-app-service
```

---

## ✅ Validation Checklist
- [ ] Git repo created and contains valid manifests
- [ ] ArgoCD app manifest applied
- [ ] App synced via ArgoCD UI or CLI
- [ ] App is running in Kubernetes cluster

---

## 🧹 Cleanup
```bash
argocd app delete demo-app --cascade
kubectl delete svc demo-app-service
kubectl delete deploy demo-app
```

---

## 🧠 Key Concepts
- GitOps deployment via ArgoCD
- ArgoCD Application CRD
- Git as the source of truth for Kubernetes state

---

## 🔁 What's Next?
Continue to [LAB03 - Helm Deployments](../LAB03-Helm-Deployments/) to learn how to deploy Helm charts using ArgoCD.

Git-driven Kubernetes. 🌱💾🚢