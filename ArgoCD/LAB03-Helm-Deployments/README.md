# LAB03: Deploying Applications with Helm Charts via Argo CD

Welcome to Lab 03! In the previous labs, you deployed applications using raw Kubernetes manifests. Now, we'll explore how to leverage Helm, the package manager for Kubernetes, in conjunction with Argo CD.

Helm charts help you define, install, and upgrade even the most complex Kubernetes applications. Argo CD has excellent built-in support for deploying applications packaged as Helm charts. This lab will guide you through deploying a public Helm chart and customizing its configuration using Argo CD and Git-managed values.

For detailed step-by-step instructions to complete this lab, please refer to **[./LAB.md](./LAB.md)**.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand what Helm is and why it's used for Kubernetes applications
- Find and use public Helm charts from repositories like Bitnami
- Configure Argo CD to deploy applications from public Helm chart repositories
- Use Git-managed custom values files to override Helm chart defaults
- Deploy and customize a Helm chart via Argo CD using GitOps practices
- Experience the GitOps workflow with Helm charts and value modifications

---

## 🧰 Prerequisites

- **Completion of LAB01 and LAB02:** Familiarity with Argo CD UI, deploying applications, and Git operations
- **Minikube and Argo CD Running:** As per the `ArgoCD/install-and-setup.md` guide
- **`kubectl` Configured:** Pointing to your Minikube cluster
- **Git Installed and Configured:** You'll need Git to manage your Helm values files
- **A Personal Git Repository Host Account:** Such as GitHub for storing your custom Helm values
- **Basic understanding of Helm concepts is helpful but not required** (the lab provides explanations)

---

## 📂 Folder Structure for This Lab

This lab provides a complete Helm values file that you'll copy to your own Git repository:

```bash
ArgoCD/LAB03-Helm-Deployments/
├── helm-values/
│   └── my-nginx-values.yaml # Complete Helm values file for nginx chart
├── README.md                # Lab overview (this file)
└── LAB.md                   # Detailed step-by-step lab instructions
```

---

## ✅ Validation Checklist

Refer to the validation checklist at the end of **[./LAB.md](./LAB.md)** after completing the lab steps.

---

## 🧹 Cleanup

Detailed cleanup instructions are provided at the end of **[./LAB.md](./LAB.md)**.

In summary:
1. Delete the Helm application from the Argo CD UI
2. Delete the namespace using `kubectl delete namespace helm-nginx-app`
3. Optionally remove the helm-values from your Git repository
4. Optionally stop Minikube

---

## ✨ Key Concepts

- **Helm:** The package manager for Kubernetes that helps manage complex applications through packaged units called charts
- **Helm Chart:** A collection of files that describe a related set of Kubernetes resources, versioned and reusable
- **Helm Repository:** A location where packaged Helm charts are stored and shared (e.g., Bitnami, Artifact Hub)
- **Helm Release:** An instance of a chart running in a Kubernetes cluster with a specific configuration
- **`values.yaml`:** Configuration files that customize Helm chart deployments by overriding default parameters
- **Argo CD Helm Support:** Argo CD can deploy Helm charts, manage releases, and track custom values stored in Git repositories

---

## 🚀 What's Next?

Congratulations! You've successfully deployed and managed a Helm chart using Argo CD and GitOps principles. You now understand how to leverage Helm's packaging capabilities within a GitOps workflow.

Proceed to **[../LAB04-GitOps-Rollback/README.md](../LAB04-GitOps-Rollback/README.md)** to learn about rollback strategies in GitOps.