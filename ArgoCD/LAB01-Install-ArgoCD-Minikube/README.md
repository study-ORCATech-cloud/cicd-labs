# LAB01 - Install ArgoCD on Minikube

## 📝 Description
This lab walks you through installing **ArgoCD** on a local **Minikube** cluster. It covers creating the required namespace, installing ArgoCD components, exposing the ArgoCD UI, and logging in to begin managing applications.

---

## 🎯 Objectives

By the end of this lab, you will:
- Install ArgoCD in a local Kubernetes environment (Minikube)
- Access the ArgoCD web UI
- Log in with default credentials
- Understand the ArgoCD architecture

---

## 🧰 Prerequisites

- Minikube installed and running
- `kubectl` and `argocd` CLI installed

---

## 🗂️ Folder Structure
```bash
ArgoCD/LAB01-Install-ArgoCD-Minikube/
├── README.md
```

---

## 🚀 Getting Started

### 1. Start Minikube
```bash
minikube start --memory=4096 --cpus=2
```

### 2. Create the ArgoCD namespace
```bash
kubectl create namespace argocd
```

### 3. Install ArgoCD components
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 4. Expose the ArgoCD API server
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### 5. Retrieve the default admin password
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
```

### 6. Login via CLI
```bash
argocd login localhost:8080 --username admin --password <retrieved-password> --insecure
```

### 7. Access ArgoCD UI
Open your browser and go to: `https://localhost:8080` (accept the insecure SSL warning)

---

## ✅ Validation Checklist
- [ ] Minikube is running
- [ ] ArgoCD installed in the `argocd` namespace
- [ ] Port-forwarding is active on port 8080
- [ ] Able to login using CLI or UI with admin credentials

---

## 🧹 Cleanup
```bash
kubectl delete namespace argocd
minikube stop
```

---

## 🧠 Key Concepts
- ArgoCD installation process and architecture
- Admin login using initial secret
- Kubernetes port-forwarding for local UI access

---

## 🔁 What's Next?
Continue to [LAB02 - K8s GitOps Deploy](../LAB02-K8s-GitOps-Deploy/) to deploy applications using Git as the source of truth.

GitOps begins with setup. 🎛️📦🚀

