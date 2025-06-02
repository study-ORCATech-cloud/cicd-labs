# LAB08: CI/CD Integration with GitOps Promotion Workflows

Welcome to Lab 08! You've mastered multi-environment GitOps workflows with manual promotion from staging to production. Now it's time to **automate the entire CI/CD pipeline** by integrating continuous integration with your GitOps promotion workflows.

In modern DevOps practices, you want to automate not just the deployment (which ArgoCD handles), but also the promotion process itself. This lab will teach you how to build end-to-end CI/CD pipelines that automatically build, test, and promote applications through your environments using GitOps principles.

For detailed step-by-step instructions to complete this lab, please refer to **[./LAB.md](./LAB.md)**.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Design and implement complete CI/CD pipelines that integrate with GitOps workflows
- Automate application builds, testing, and image creation using GitHub Actions
- Implement automated promotion workflows that update GitOps repositories
- Configure CI pipelines to automatically promote changes from staging to production
- Handle image versioning, tagging, and manifest updates in GitOps repositories
- Set up proper CI triggers, approval gates, and rollback mechanisms
- Integrate container registries with CI/CD and ArgoCD workflows
- Implement security scanning and quality gates in automated pipelines
- Understand the separation of concerns between CI (build/test) and CD (deploy) systems

---

## 🧰 Prerequisites

- **Completion of LAB01-LAB07:** Strong foundation in ArgoCD operations and multi-environment GitOps workflows
- **Minikube and Argo CD Running:** As per the `ArgoCD/install-and-setup.md` guide
- **`kubectl` Configured:** Pointing to your Minikube cluster with sufficient resources
- **Git and GitHub Account:** For CI/CD pipeline integration and container registry access
- **GitHub Repository:** Either reuse from previous labs or create new repository for this lab
- **Docker Hub Account:** For container image storage (free account works fine)
- **Basic CI/CD Knowledge:** Understanding of build pipelines, testing, and deployment concepts

---

## 📂 Folder Structure for This Lab

This lab provides complete examples for CI/CD integration with GitOps workflows:

```bash
ArgoCD/LAB08-CI-Promote-To-ArgoCD/
├── app/
│   ├── main.py                       # Sample Python Flask application
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Container build configuration
│   └── tests/
│       ├── test_app.py              # Unit tests for the application
│       └── test_requirements.txt    # Test dependencies
├── .github/
│   └── workflows/
│       ├── ci-build-test.yml        # CI pipeline for build and test
│       ├── promote-to-staging.yml   # Automated staging promotion
│       └── promote-to-production.yml # Production promotion workflow
├── gitops-repo/
│   ├── environments/
│   │   ├── staging/
│   │   │   ├── deployment.yaml      # Staging deployment with image tag
│   │   │   └── kustomization.yaml   # Kustomize configuration for staging
│   │   └── production/
│   │       ├── deployment.yaml      # Production deployment with image tag
│   │       └── kustomization.yaml   # Kustomize configuration for production
│   └── argocd-apps/
│       ├── staging-app.yaml         # ArgoCD application for staging
│       └── production-app.yaml      # ArgoCD application for production
├── scripts/
│   ├── update-image-tag.sh          # Script for updating image tags in GitOps repo
│   └── promote-environment.sh       # Script for environment promotion
├── README.md                        # Lab overview (this file)
└── LAB.md                           # Detailed step-by-step lab instructions
```

---

## ✅ Validation Checklist

Refer to the validation checklist at the end of **[./LAB.md](./LAB.md)** after completing the lab steps.

---

## 🧹 Cleanup

Detailed cleanup instructions are provided at the end of **[./LAB.md](./LAB.md)**.

In summary:
1. Delete CI/CD applications from the Argo CD UI
2. Disable or delete GitHub Actions workflows
3. Delete the staging and production namespaces using kubectl
4. Optionally clean up Docker images and GitHub repository changes
5. Optionally stop Minikube

---

## ✨ Key Concepts

- **CI/CD Integration:** Seamless connection between continuous integration and GitOps-based continuous deployment
- **Automated Promotion:** Using CI pipelines to automatically promote applications between environments
- **Image Versioning:** Systematic approach to tagging and managing container image versions
- **GitOps Repository Updates:** Programmatic updates to GitOps repositories from CI pipelines
- **Pipeline Triggers:** Configuring appropriate triggers for build, test, and promotion workflows
- **Approval Gates:** Implementing human approval steps in automated promotion pipelines
- **Container Registry Integration:** Connecting CI builds with container registries and ArgoCD deployments
- **Security Scanning:** Integrating security and vulnerability scanning into CI/CD pipelines
- **Quality Gates:** Implementing automated testing and quality checks before promotion
- **Rollback Automation:** Automated rollback mechanisms when deployments fail
- **Branch-based Workflows:** Using Git branches to trigger different pipeline behaviors
- **Environment Promotion:** Systematic progression of changes through development, staging, and production
- **Separation of Concerns:** Clear division between CI (build/test) and CD (deploy) responsibilities

---

## 🚀 What's Next?

Congratulations! You've mastered end-to-end CI/CD integration with GitOps workflows. You understand how to automate the complete software delivery pipeline from code commit to production deployment.

Proceed to **[../LAB09-Notifications/README.md](../LAB09-Notifications/README.md)** to learn how to implement comprehensive monitoring and alerting for your CI/CD and GitOps workflows.