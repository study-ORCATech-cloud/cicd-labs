# LAB07: Multi-Environment GitOps - Staging to Production

Welcome to Lab 07! You've mastered individual ArgoCD deployments and secrets management. Now it's time to tackle one of the most critical production challenges: **managing multiple environments with consistent, safe promotion workflows**.

In real-world scenarios, you never deploy directly to production. Instead, you follow a promotion pipeline: development → staging → production. Each environment should be isolated, configurable, and follow GitOps principles. This lab will teach you how to implement robust multi-environment workflows using ArgoCD with folder-based and branch-based strategies.

For detailed step-by-step instructions to complete this lab, please refer to **[./LAB.md](./LAB.md)**.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Design and implement multi-environment GitOps workflows with staging and production
- Use folder-based and branch-based strategies for environment separation
- Configure environment-specific settings and resource limits
- Implement safe promotion workflows from staging to production
- Set up ArgoCD applications for multiple environments with proper isolation
- Handle environment-specific secrets and configurations
- Understand progressive deployment strategies and rollback procedures
- Apply production-ready multi-environment best practices

---

## 🧰 Prerequisites

- **Completion of LAB01-LAB06:** Strong foundation in ArgoCD operations, GitOps workflows, and secrets management
- **Minikube and Argo CD Running:** As per the `ArgoCD/install-and-setup.md` guide
- **`kubectl` Configured:** Pointing to your Minikube cluster with sufficient resources
- **Git Installed and Configured:** For managing multi-environment repositories
- **A Personal Git Repository:** To demonstrate promotion workflows (can reuse from previous labs)
- **Understanding of environment separation:** Helpful background in staging/production concepts

---

## 📂 Folder Structure for This Lab

This lab provides complete examples for multi-environment GitOps workflows:

```bash
ArgoCD/LAB07-Staging-To-Production/
├── environments/
│   ├── staging/
│   │   ├── deployment.yaml           # Staging-specific deployment configuration
│   │   ├── service.yaml              # Staging service configuration  
│   │   ├── configmap.yaml            # Staging environment variables
│   │   └── hpa.yaml                  # Staging horizontal pod autoscaler
│   ├── production/
│   │   ├── deployment.yaml           # Production-specific deployment configuration
│   │   ├── service.yaml              # Production service configuration
│   │   ├── configmap.yaml            # Production environment variables
│   │   └── hpa.yaml                  # Production horizontal pod autoscaler
│   └── common/
│       ├── namespace-staging.yaml    # Staging namespace definition
│       └── namespace-production.yaml # Production namespace definition
├── argocd-apps/
│   ├── staging-app.yaml              # ArgoCD application for staging
│   └── production-app.yaml           # ArgoCD application for production
├── README.md                         # Lab overview (this file)
└── LAB.md                            # Detailed step-by-step lab instructions
```

---

## ✅ Validation Checklist

Refer to the validation checklist at the end of **[./LAB.md](./LAB.md)** after completing the lab steps.

---

## 🧹 Cleanup

Detailed cleanup instructions are provided at the end of **[./LAB.md](./LAB.md)**.

In summary:
1. Delete staging and production applications from the Argo CD UI
2. Delete the staging and production namespaces using kubectl
3. Optionally clean up your Git repository changes
4. Optionally stop Minikube

---

## ✨ Key Concepts

- **Multi-Environment Strategy:** Systematic approach to managing development, staging, and production environments
- **Environment Separation:** Techniques for isolating environments using namespaces, clusters, or repositories
- **Folder-Based Environments:** Using Git folder structure to manage environment-specific configurations
- **Branch-Based Environments:** Using Git branches to represent different environment states
- **Promotion Workflows:** Systematic process of moving changes from one environment to another
- **Environment-Specific Configuration:** Managing different settings, resources, and secrets per environment
- **Progressive Deployment:** Gradual rollout strategies that minimize risk in production deployments
- **Environment Parity:** Maintaining consistency between environments while allowing necessary differences
- **Blue-Green Deployments:** Advanced deployment strategy using environment switching
- **GitOps Promotion:** Git-based workflows for promoting changes between environments
- **Environment Governance:** Policies and controls for managing multi-environment deployments
- **Rollback Strategies:** Safe procedures for reverting changes across multiple environments

---

## 🚀 What's Next?

Congratulations! You've mastered multi-environment GitOps workflows with safe promotion strategies. You understand how to structure environments, configure environment-specific settings, and implement robust promotion workflows.

Proceed to **[../LAB08-CI-Promote-To-ArgoCD/README.md](../LAB08-CI-Promote-To-ArgoCD/README.md)** to learn how to integrate CI pipelines with your GitOps promotion workflows.