# LAB02: Deploying Your Own Application from Git with Argo CD

Welcome to Lab 02! In the previous lab, you deployed a sample application from a public Git repository using Argo CD. Now, it's time to take the next step: deploying an application that you manage in your own Git repository.

This lab will guide you through deploying a provided Python Flask application using your own Git repository and Argo CD. You'll learn how to build Docker images, modify Kubernetes manifests, and set up a complete GitOps workflow.

For detailed step-by-step instructions to complete this lab, please refer to **[./LAB.md](./LAB.md)**.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Build and push a Docker image from provided application code
- Use provided Kubernetes manifests for your application deployment
- Create and configure your own Git repository for GitOps
- Configure Argo CD to deploy applications from your personal Git repository
- Understand how Argo CD detects and synchronizes changes from Git
- Experience the complete GitOps workflow with your own application

---

## 🧰 Prerequisites

- **Completion of LAB01:** You should be familiar with the Argo CD UI and basic operations
- **Minikube and Argo CD Running:** As per the `ArgoCD/install-and-setup.md` guide
- **`kubectl` Configured:** Pointing to your Minikube cluster
- **Git Installed and Configured:** You'll need Git to manage your application code and push it to a repository
- **A Personal Git Repository Host Account:** Such as GitHub, GitLab, or Bitbucket (this lab uses GitHub for examples)
- **Docker Installed and Running:** You'll need Docker to build your application image
- **(Optional but Recommended) Docker Hub Account:** Or an account with another container registry
- **Basic understanding of Docker and Kubernetes concepts**

---

## 📂 Folder Structure for This Lab

This lab provides complete application code and Kubernetes manifests that you'll copy to your own Git repository:

```bash
ArgoCD/LAB02-K8s-GitOps-Deploy/
├── app/
│   ├── main.py         # Complete Python Flask application
│   └── Dockerfile      # Complete Dockerfile to containerize the app
├── k8s-manifests/
│   ├── deployment.yaml # Complete Kubernetes Deployment manifest
│   └── service.yaml    # Complete Kubernetes Service manifest
├── README.md           # Lab overview (this file)
└── LAB.md              # Detailed step-by-step lab instructions
```

---

## ✅ Validation Checklist

Refer to the validation checklist at the end of **[./LAB.md](./LAB.md)** after completing the lab steps.

---

## 🧹 Cleanup

Detailed cleanup instructions are provided at the end of **[./LAB.md](./LAB.md)**.

In summary:
1. Delete the application from the Argo CD UI
2. Delete the namespace using `kubectl delete namespace my-custom-app-ns`
3. Optionally delete the Docker image and Git repository
4. Optionally stop Minikube

---

## ✨ Key Concepts

- **GitOps Workflow:** Using Git as the single source of truth for application deployment
- **Container Registry:** A service that stores and distributes Docker images (like Docker Hub)
- **Kubernetes Manifests:** YAML files that define Kubernetes resources like Deployments and Services
- **Argo CD Application:** A resource that tells Argo CD what to deploy, from where, and to which destination
- **Sync Status:** Indicates whether the live state matches the desired state in Git
- **Health Status:** Indicates whether the deployed resources are healthy and running properly

---

## 🚀 What's Next?

Congratulations! You've successfully set up a GitOps workflow for your own application using Argo CD. You now understand how to containerize applications, manage Kubernetes manifests in Git, and deploy using GitOps principles.

Proceed to **[../LAB03-Helm-Deployments/README.md](../LAB03-Helm-Deployments/README.md)** to explore how to use Helm charts with Argo CD.