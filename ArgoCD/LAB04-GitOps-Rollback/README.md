# LAB04: GitOps Rollback Strategies with Argo CD

Welcome to Lab 04! In the previous labs, you've learned to deploy applications using ArgoCD with raw manifests and Helm charts. Now, we'll explore one of the most powerful aspects of GitOps: **safe and auditable rollbacks**.

In traditional deployment methods, rolling back can be complex and error-prone. GitOps changes this by leveraging Git's inherent version control capabilities. Every change is tracked, and every previous state can be restored with confidence. This lab will teach you multiple rollback strategies using ArgoCD.

For detailed step-by-step instructions to complete this lab, please refer to **[./LAB.md](./LAB.md)**.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand the concept of GitOps rollbacks and why they're safer than traditional approaches
- Use ArgoCD's application history to view previous deployments and their Git commit references
- Perform rollbacks using ArgoCD UI with revision selection
- Execute rollbacks via ArgoCD CLI commands
- Use Git-based rollbacks by reverting commits and syncing changes
- Understand the difference between ArgoCD rollbacks and Git reverts
- Experience the complete rollback workflow from detection to resolution

---

## 🧰 Prerequisites

- **Completion of LAB01, LAB02, and LAB03:** Familiarity with ArgoCD operations and Git workflows
- **Minikube and Argo CD Running:** As per the `ArgoCD/install-and-setup.md` guide
- **`kubectl` Configured:** Pointing to your Minikube cluster
- **Git Installed and Configured:** For managing rollback scenarios
- **A Personal Git Repository:** To practice rollback operations (can reuse from previous labs)
- **ArgoCD CLI Installed (Optional):** For command-line rollback operations

---

## 📂 Folder Structure for This Lab

This lab provides complete application manifests representing different versions:

```bash
ArgoCD/LAB04-GitOps-Rollback/
├── app-versions/
│   ├── v1-deployment.yaml    # Version 1 of the application 
│   ├── v2-deployment.yaml    # Version 2 of the application (with issues)
│   └── v3-deployment.yaml    # Version 3 of the application (fixed)
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
1. Delete the rollback application from the Argo CD UI
2. Delete the namespace using `kubectl delete namespace rollback-demo-app`
3. Optionally clean up your Git repository changes
4. Optionally stop Minikube

---

## ✨ Key Concepts

- **GitOps Rollback:** Using Git's version control capabilities to safely revert application states
- **ArgoCD Application History:** Track of all sync operations and their corresponding Git commits
- **Revision-based Rollback:** Rolling back to a specific ArgoCD revision using the UI or CLI
- **Git-based Rollback:** Using Git revert/reset commands to change the desired state in the repository
- **Immutable Deployments:** Each deployment is a snapshot that can be exactly reproduced
- **Audit Trail:** Complete history of who changed what and when in both Git and ArgoCD
- **Rollback vs Revert:** Understanding the difference between ArgoCD internal rollbacks and Git commit reverts

---

## 🚀 What's Next?

Congratulations! You've mastered GitOps rollback strategies and understand how to safely recover from problematic deployments. You now have the confidence to handle production incidents using GitOps principles.

Proceed to **[../LAB05-Sync-Policy-Auto-Sync/README.md](../LAB05-Sync-Policy-Auto-Sync/README.md)** to learn about automated synchronization policies in ArgoCD.