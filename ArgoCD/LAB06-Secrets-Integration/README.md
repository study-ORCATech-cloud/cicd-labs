# LAB06: Secrets Management in GitOps with ArgoCD

Welcome to Lab 06! In the previous labs, you've deployed applications and configured sync policies, but we've avoided one critical production requirement: **managing secrets securely**. 

In traditional deployments, secrets are often handled manually or through configuration management tools. However, GitOps requires everything to be in Git, which creates a security challenge: how do you store sensitive data like passwords, API keys, and certificates in Git repositories safely? This lab will teach you practical approaches to secrets management in GitOps workflows.

For detailed step-by-step instructions to complete this lab, please refer to **[./LAB.md](./LAB.md)**.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand the security challenges of managing secrets in GitOps workflows
- Install and configure Sealed Secrets for encrypting secrets in Git repositories
- Create, seal, and deploy encrypted secrets using ArgoCD
- Implement secure secrets workflows that follow GitOps principles
- Understand alternative secrets management approaches for production environments
- Apply secrets security best practices in real-world scenarios
- Troubleshoot common secrets management issues in ArgoCD

---

## 🧰 Prerequisites

- **Completion of LAB01-LAB05:** Strong understanding of ArgoCD operations and GitOps workflows
- **Minikube and Argo CD Running:** As per the `ArgoCD/install-and-setup.md` guide
- **`kubectl` Configured:** Pointing to your Minikube cluster
- **Git Installed and Configured:** For managing encrypted secrets in repositories
- **A Personal Git Repository:** To store encrypted secrets (can reuse from previous labs)
- **Basic understanding of Kubernetes secrets:** Helpful but not required

---

## 📂 Folder Structure for This Lab

This lab provides complete examples for secrets management with GitOps:

```bash
ArgoCD/LAB06-Secrets-Integration/
├── secrets-app/
│   ├── deployment.yaml           # Application that uses secrets
│   ├── service.yaml              # Service for the secrets demo app
│   ├── regular-secret.yaml       # Example of a regular Kubernetes secret
│   └── sealed-secret.yaml        # Example of a Sealed Secret
├── README.md                     # Lab overview (this file)
└── LAB.md                        # Detailed step-by-step lab instructions
```

---

## ✅ Validation Checklist

Refer to the validation checklist at the end of **[./LAB.md](./LAB.md)** after completing the lab steps.

---

## 🧹 Cleanup

Detailed cleanup instructions are provided at the end of **[./LAB.md](./LAB.md)**.

In summary:
1. Delete the secrets application from the Argo CD UI
2. Delete the namespace using `kubectl delete namespace secrets-demo-app`
3. Remove the Sealed Secrets controller (optional)
4. Optionally clean up your Git repository changes
5. Optionally stop Minikube

---

## ✨ Key Concepts

- **Secrets in GitOps:** The challenge of storing sensitive data in Git repositories while maintaining security
- **Sealed Secrets:** A Kubernetes controller that encrypts secrets so they can be safely stored in Git
- **Secret Encryption:** Process of converting plain-text secrets into encrypted form using public-key cryptography
- **Controller-based Decryption:** Only the Sealed Secrets controller in the cluster can decrypt sealed secrets
- **GitOps-Compatible Security:** Approaches that maintain both security and the GitOps principle of "everything in Git"
- **Key Rotation:** Process of updating encryption keys and re-sealing secrets for enhanced security
- **External Secrets Operators:** Alternative approaches using external secret stores (Vault, AWS Secrets Manager, etc.)
- **Secrets Lifecycle Management:** Handling creation, rotation, and deletion of secrets in GitOps workflows

---

## 🚀 What's Next?

Congratulations! You've mastered secure secrets management in GitOps workflows. You understand how to encrypt sensitive data for safe storage in Git repositories while maintaining the benefits of GitOps automation.

Proceed to **[../LAB07-Staging-To-Production/README.md](../LAB07-Staging-To-Production/README.md)** to learn about managing multiple environments with ArgoCD.