# LAB09 - Notifications

## 📝 Description
This lab covers how to enable and configure **ArgoCD Notifications** to alert teams about application sync events, health changes, or failures via Slack, email, or other channels.

---

## 🎯 Objectives
- Install and configure ArgoCD Notifications
- Send alerts on sync status, health, or deployment
- Integrate with Slack or external webhook receivers

---

## 🧰 Prerequisites
- Completion of LAB08
- ArgoCD running on a cluster
- Slack webhook URL (or other alert channels)

---

## 🗂️ Folder Structure
```bash
ArgoCD/LAB09-Notifications/
├── configmap-notifications.yaml
├── secret-notifiers.yaml
├── trigger-binding.yaml
└── README.md
```

---

## 🚀 Getting Started

### 1. Install ArgoCD Notifications controller
```bash
kubectl apply -f https://raw.githubusercontent.com/argoproj-labs/argocd-notifications/stable/manifests/install.yaml
```

### 2. Create notifier secret with Slack webhook
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: argocd-notifications-secret
  namespace: argocd
stringData:
  slack-token: <SLACK_WEBHOOK_URL>
```
```bash
kubectl apply -f secret-notifiers.yaml
```

### 3. Configure templates and triggers
Apply the ConfigMap:
```bash
kubectl apply -f configmap-notifications.yaml
kubectl apply -f trigger-binding.yaml
```

---

## ✅ Validation Checklist
- [ ] Notifications controller installed
- [ ] Slack token secret applied
- [ ] Triggers and templates created
- [ ] Notification sent on app change

---

## 🧹 Cleanup
```bash
kubectl delete secret argocd-notifications-secret -n argocd
kubectl delete configmap argocd-notifications-cm -n argocd
kubectl delete app myapp
```

---

## 🧠 Key Concepts
- ArgoCD Notification CRs: templates, triggers, bindings
- External alert channels (Slack, email, webhooks)
- Event-driven alerting for GitOps workflows

---

## 🔁 What's Next?
Continue to [LAB10 - RBAC And SSO Security](../LAB10-RBAC-And-SSO-Security/) to secure your ArgoCD instance.

Alert the team. Ship with confidence. 🔔🛰️📣