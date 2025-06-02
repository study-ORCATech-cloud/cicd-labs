# LAB05: ArgoCD Sync Policies and Automation

Welcome to Lab 05! In the previous labs, you've been manually synchronizing applications in ArgoCD. Now, we'll explore one of the most powerful features of GitOps: **automated synchronization policies**.

In production environments, manually syncing every change isn't practical. ArgoCD's sync policies allow you to automate deployments, enable self-healing capabilities, and ensure your cluster always reflects the desired state in Git. This lab will teach you how to configure and use these automation features effectively.

For detailed step-by-step instructions to complete this lab, please refer to **[./LAB.md](./LAB.md)**.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand the difference between manual and automated sync policies
- Configure auto-sync policies for continuous deployment
- Implement self-healing to automatically fix configuration drift
- Use automated pruning to remove orphaned resources
- Configure sync options like retry policies and sync windows
- Test different sync scenarios and understand their impact
- Make informed decisions about when to use manual vs automated sync

---

## 🧰 Prerequisites

- **Completion of LAB01-LAB04:** Strong familiarity with ArgoCD operations and Git workflows
- **Minikube and Argo CD Running:** As per the `ArgoCD/install-and-setup.md` guide
- **`kubectl` Configured:** Pointing to your Minikube cluster
- **Git Installed and Configured:** For triggering automated sync scenarios
- **A Personal Git Repository:** To test automated sync behaviors (can reuse from previous labs)
- **Understanding of GitOps principles:** From previous labs

---

## 📂 Folder Structure for This Lab

This lab provides complete application manifests to demonstrate sync policies:

```bash
ArgoCD/LAB05-Sync-Policy-Auto-Sync/
├── sync-demo-app/
│   ├── deployment.yaml       # Application deployment manifest
│   ├── service.yaml          # Service manifest  
│   └── configmap.yaml        # ConfigMap for testing sync scenarios
├── README.md                 # Lab overview (this file)
└── LAB.md                    # Detailed step-by-step lab instructions
```

---

## ✅ Validation Checklist

Refer to the validation checklist at the end of **[./LAB.md](./LAB.md)** after completing the lab steps.

---

## 🧹 Cleanup

Detailed cleanup instructions are provided at the end of **[./LAB.md](./LAB.md)**.

In summary:
1. Delete the sync demo application from the Argo CD UI
2. Delete the namespace using `kubectl delete namespace sync-demo-app`
3. Optionally clean up your Git repository changes
4. Optionally stop Minikube

---

## ✨ Key Concepts

- **Manual Sync:** Default mode where changes must be manually synchronized via UI or CLI
- **Auto Sync:** Automatically synchronizes when Git repository changes are detected
- **Self-Healing:** Automatically reverts manual changes to Kubernetes resources back to Git state
- **Automated Pruning:** Automatically removes resources that are no longer defined in Git
- **Sync Options:** Additional configurations like retry policies, sync windows, and resource ordering
- **Configuration Drift:** When the actual cluster state differs from the desired state in Git
- **Sync Waves:** Control the order in which resources are applied during synchronization
- **Sync Windows:** Time-based restrictions on when automatic synchronization can occur

---

## 🚀 What's Next?

Congratulations! You've mastered ArgoCD sync policies and understand how to implement fully automated GitOps workflows. You can now set up continuous deployment pipelines that respond automatically to Git changes while maintaining safety and control.

Proceed to **[../LAB06-Secrets-Integration/README.md](../LAB06-Secrets-Integration/README.md)** to learn about integrating secrets management with ArgoCD.