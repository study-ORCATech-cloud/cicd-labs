# LAB01: Deploying Your First Application with Argo CD

Welcome to your first hands-on lab with Argo CD! Now that you have Minikube and Argo CD installed (as per the `ArgoCD/install-and-setup.md` guide), this lab will guide you through deploying a sample application using Argo CD. You'll see the core GitOps flow in action: Argo CD will pull Kubernetes manifests from a public Git repository and deploy them to your Minikube cluster.

We will use the standard Kubernetes "guestbook" application for this demonstration, whose manifests are publicly hosted by the Argo CD project.

For detailed step-by-step instructions to complete this lab, please refer to **[./LAB.md](./LAB.md)**.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand how to create a new application within the Argo CD UI.
- Connect Argo CD to a public Git repository containing Kubernetes manifests.
- Deploy a sample application (Kubernetes guestbook) to your Minikube cluster using Argo CD.
- Observe the application's status, components, and synchronization process in Argo CD.
- Access the deployed application running in Minikube.
- Understand the basic cleanup process for an Argo CD application.

---

## 🧰 Prerequisites

-   **Completion of the `ArgoCD/install-and-setup.md` guide:**
    *   Minikube must be running.
    *   `kubectl` must be configured to communicate with your Minikube cluster.
    *   Argo CD must be installed in the `argocd` namespace in Minikube.
    *   You must be able to access the Argo CD UI via port-forwarding (e.g., on `https://localhost:8080/`) and log in as `admin`.
-   **Familiarity with basic Kubernetes concepts** (Namespace, Pod, Deployment, Service) is helpful but not strictly required to follow the steps.

---

## 📂 Folder Structure for This Lab

This lab primarily involves interacting with the Argo CD UI and `kubectl`. The application manifests are pulled directly from a public Git repository, so no additional files are required for this lab.

```bash
ArgoCD/LAB01-Deploy-First-Application/
├── README.md         # Lab overview, objectives, prerequisites etc. (this file)
└── LAB.md            # Detailed step-by-step lab instructions
```

---

## ✅ Validation Checklist

Refer to the validation checklist at the end of **[./LAB.md](./LAB.md)** after completing the lab steps.

---

## 🧹 Cleanup

Detailed cleanup instructions are provided at the end of **[./LAB.md](./LAB.md)**.

In summary:
1.  Delete the `guestbook` application from the Argo CD UI.
2.  Delete the `guestbook` namespace using `kubectl delete namespace guestbook`.
3.  Optionally, stop Minikube (`minikube stop`) and the `kubectl port-forward` command.

---

## ✨ Key Concepts

-   **Kubernetes (`k8s`):** An open-source system for automating deployment, scaling, and management of containerized applications.
-   **Minikube:** A tool to run a single-node Kubernetes cluster locally for development and testing.
-   **`kubectl`:** The command-line interface for interacting with a Kubernetes cluster.
-   **GitOps:** A way of implementing Continuous Delivery for cloud-native applications. It uses Git as a single source of truth for declarative infrastructure and applications.
-   **Argo CD:** A declarative, GitOps continuous delivery tool for Kubernetes. It monitors Git repositories and automatically deploys and synchronizes application changes to your Kubernetes cluster.
    *   **Application:** The core Argo CD resource representing a set of Kubernetes manifests to be deployed.
    *   **Sync:** The process of reconciling the live state in the cluster with the desired state in Git.
    *   **Health Status:** Argo CD assesses the health of your deployed applications based on Kubernetes resource status.

---

## 🚀 What's Next?

Congratulations! You've successfully deployed your first application using Argo CD and experienced the basic GitOps workflow. This foundational understanding will be built upon in the following labs.

Proceed to **[../LAB02-K8s-GitOps-Deploy/README.md](../LAB02-K8s-GitOps-Deploy/README.md)** to learn how to deploy applications from your own Git repository.

