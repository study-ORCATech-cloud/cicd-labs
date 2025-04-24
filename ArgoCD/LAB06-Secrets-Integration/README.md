# LAB06 - Secrets Integration

## 📝 Description
This lab demonstrates how to manage secrets with ArgoCD using tools like **Sealed Secrets** or **External Secrets Operator**, allowing secure delivery of sensitive data to Kubernetes.

---

## 🎯 Objectives
- Understand secret management challenges in GitOps
- Use sealed secrets or external secrets
- Deploy secrets securely via Git

---

## 🧰 Prerequisites
- Completion of LAB05
- Helm and `kubeseal` CLI installed (for Sealed Secrets)
- ArgoCD up and running

---

## 🗂️ Folder Structure
```bash
ArgoCD/LAB06-Secrets-Integration/
├── secrets/
│   └── sealedsecret.yaml
├── argo-app.yaml
└── README.md
```

---

## 🚀 Getting Started

### 1. Install Sealed Secrets controller
```bash
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.21.0/controller.yaml
```

### 2. Create a Kubernetes Secret locally
```bash
kubectl create secret generic demo-secret --from-literal=password=supersecret --dry-run=client -o yaml > secret.yaml
```

### 3. Seal the secret
```bash
kubeseal < secret.yaml > secrets/sealedsecret.yaml --controller-namespace kube-system --format yaml
```

### 4. Push sealed secret to Git and sync
Update ArgoCD application to use `secrets/` path and sync.

---

## ✅ Validation Checklist
- [ ] Sealed secret file pushed to Git
- [ ] ArgoCD synced and sealed secret deployed
- [ ] Secret appears in Kubernetes after sealing

---

## 🧹 Cleanup
```bash
kubectl delete sealedsecret demo-secret
kubectl delete secret demo-secret
```

---

## 🧠 Key Concepts
- Sealed Secrets encrypt secrets for safe Git storage
- Only the controller can decrypt sealed secrets
- GitOps-compatible secret management

---

## 🔁 What's Next?
Continue to [LAB07 - Staging To Production](../LAB07-Staging-To-Production/) for multi-env GitOps workflows.

Secrets in Git? Only if they’re sealed. 🔐📄🚀