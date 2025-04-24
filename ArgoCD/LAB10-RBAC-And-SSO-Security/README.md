# LAB10 - RBAC And SSO Security

## 📝 Description
This lab focuses on securing ArgoCD with **Role-Based Access Control (RBAC)** and enabling **Single Sign-On (SSO)** for centralized authentication. You'll learn how to manage users and restrict access to projects and applications.

---

## 🎯 Objectives
- Understand ArgoCD RBAC structure and roles
- Configure ArgoCD to use SSO (e.g., GitHub, Google)
- Secure sensitive application and project access

---

## 🧰 Prerequisites
- Completion of LAB09
- ArgoCD admin access
- OAuth provider credentials (GitHub, Google, Okta, etc.)

---

## 🗂️ Folder Structure
```bash
ArgoCD/LAB10-RBAC-And-SSO-Security/
├── argocd-rbac-cm.yaml
├── argocd-cm-sso.yaml
└── README.md
```

---

## 🚀 Getting Started

### 1. Configure RBAC policy
Edit `argocd-rbac-cm.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
  labels:
    app.kubernetes.io/part-of: argocd
  annotations:
    managed-by: ArgoCD
    argocd.argoproj.io/config: "true"
data:
  policy.csv: |
    g, devs, role:readonly
    g, admins, role:admin
```
```bash
kubectl apply -f argocd-rbac-cm.yaml
```

### 2. Configure SSO integration
Update `argocd-cm-sso.yaml` with your OAuth credentials:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
  labels:
    app.kubernetes.io/part-of: argocd
  annotations:
    managed-by: ArgoCD
    argocd.argoproj.io/config: "true"
data:
  url: https://argocd.example.com
  dex.config: |
    connectors:
    - type: github
      id: github
      name: GitHub
      config:
        clientID: $GITHUB_CLIENT_ID
        clientSecret: $GITHUB_CLIENT_SECRET
        orgs:
        - name: your-org-name
```
```bash
kubectl apply -f argocd-cm-sso.yaml
```

---

## ✅ Validation Checklist
- [ ] RBAC config map applied and user roles validated
- [ ] SSO login page accessible via ArgoCD UI
- [ ] OAuth login successful and RBAC enforced

---

## 🧹 Cleanup
```bash
kubectl delete configmap argocd-cm -n argocd
kubectl delete configmap argocd-rbac-cm -n argocd
```

---

## 🧠 Key Concepts
- Role-based access and multi-user security
- OAuth and SSO provider integration
- Secure GitOps access workflows

---

## 🔁 What's Next?
You’ve completed all ArgoCD labs! 🎉 Time to explore real-world GitOps pipelines and integrate monitoring and cost control tools.

Lock it down. Log in right. 🔐🧑‍💼🌐