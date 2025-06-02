# LAB03: Deploying Applications with Helm Charts via Argo CD

Welcome to Lab 03! In the previous labs, you deployed applications using raw Kubernetes manifests. Now, we'll explore how to leverage Helm, the package manager for Kubernetes, in conjunction with Argo CD.

Helm charts help you define, install, and upgrade even the most complex Kubernetes applications. Argo CD has excellent built-in support for deploying applications packaged as Helm charts. This lab will guide you through deploying a public Helm chart and customizing its configuration using Argo CD.

For detailed step-by-step instructions to complete this lab, please refer to **[./LAB.md](./LAB.md)**.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand what Helm is and why it's used.
- Find and inspect public Helm charts from repositories like Bitnami.
- Configure Argo CD to deploy an application from a public Helm chart repository.
- Specify a target Helm chart version.
- Override default Helm chart values directly within the Argo CD Application manifest/UI.
- (If included in `LAB.md`) Store custom Helm values in your Git repository and configure Argo CD to use them.
- Observe the Kubernetes resources created by the Helm chart via Argo CD.
- Access the application deployed by the Helm chart.

---

## 🧰 Prerequisites

- **Completion of LAB01 and LAB02:** Familiarity with Argo CD UI, deploying applications, and basic Git operations.
- **Minikube and Argo CD Running:** As per the `ArgoCD/install-and-setup.md` guide.
- **`kubectl` Configured:** Pointing to your Minikube cluster.
- **Git Installed and Configured (if storing values in Git):** ([Download Git](https://git-scm.com/downloads)).
- **A Personal Git Repository Host Account (if storing values in Git):** Such as GitHub ([github.com](https://github.com)).
- **Basic understanding of Helm concepts (Chart, Repository, Release, Values) is helpful.** (The lab will provide brief explanations).

---

## 📂 Folder Structure for This Lab

Depending on the chosen approach in `LAB.md` (direct value overrides vs. Git-managed values):

**Scenario 1: Overriding Helm values directly in Argo CD Application spec**
```bash
ArgoCD/LAB03-Helm-Deployments/
├── README.md         # Lab overview, objectives, etc. (this file)
├── LAB.md            # Detailed step-by-step lab instructions
└── solutions.md      # Recap of Argo CD configuration and value overrides
```

**Scenario 2: Managing custom Helm values via Git (Recommended for GitOps)**
```bash
ArgoCD/LAB03-Helm-Deployments/
├── helm-values/      # Directory in your Git repo for custom values files
│   └── my-chart-values.yaml # Example custom values (with TODOs)
├── README.md         # Lab overview, objectives, etc. (this file)
├── LAB.md            # Detailed step-by-step lab instructions
└── solutions.md      # Recap of Argo CD config & solutions for values.yaml TODOs
```
*(This lab will primarily focus on Scenario 2, as it aligns better with GitOps best practices.)*

---

## ✨ Key Concepts

-   **Helm:** The package manager for Kubernetes. Helps manage complex applications through packaged units called charts.
-   **Helm Chart:** A collection of files that describe a related set of Kubernetes resources. Charts are versioned.
-   **Helm Repository:** A location where packaged Helm charts can be stored and shared (e.g., Bitnami, Artifact Hub).
-   **Release:** An instance of a chart running in a Kubernetes cluster.
-   **`values.yaml`:** The default configuration file for a Helm chart. Users can provide their own `values.yaml` files or override specific parameters to customize a chart deployment.
-   **Argo CD Helm Support:** Argo CD can connect to Helm repositories, render charts with custom values (from Git or directly in the Application spec), and manage the lifecycle of Helm releases.

---

## ✅ Validation Checklist & 🧹 Cleanup

Refer to the Validation Checklist and Cleanup sections at the end of **[./LAB.md](./LAB.md)** after completing the lab steps.

---

## 🚀 What's Next?

After mastering Helm deployments with Argo CD, you'll be ready for more advanced topics like GitOps rollbacks and different synchronization strategies.

Proceed to **[../LAB04-GitOps-Rollback/README.md](../LAB04-GitOps-Rollback/README.md)** (once created).